from apscheduler.schedulers.background import BackgroundScheduler
from app import app, db
from app.models import Flight, PriceRecord, FlightPreference, User
from app.services.amadeus_client import AmadeusClient
from app.services.notification_service import NotificationService
from datetime import datetime

scheduler = BackgroundScheduler()
notification_service = NotificationService()

def check_flight_prices():
    with app.app_context():
        flights = Flight.query.all()
        amadeus_client = AmadeusClient()

        for flight in flights:
            flight_offers = amadeus_client.search_flights(
                origin=flight.origin,
                destination=flight.destination,
                departure_date=flight.departure_date.strftime('%Y-%m-%d'),
                return_date=flight.return_date.strftime('%Y-%m-%d') if flight.return_date else None
            )

            if flight_offers:
                new_price = float(flight_offers[0]['price']['total'])
                
                last_price_record = PriceRecord.query.filter_by(flight_id=flight.id).order_by(PriceRecord.timestamp.desc()).first()

                if last_price_record:
                    price_difference = last_price_record.price - new_price
                    if price_difference > 0:
                        # Price drop detected, send notifications
                        preferences = FlightPreference.query.filter_by(flight_id=flight.id).all()
                        for preference in preferences:
                            user = User.query.get(preference.user_id)
                            flight_info = {
                                "origin": flight.origin,
                                "destination": flight.destination,
                                "departure_date": flight.departure_date.strftime('%Y-%m-%d'),
                                "return_date": flight.return_date.strftime('%Y-%m-%d') if flight.return_date else None
                            }
                            notification_service.send_price_drop_alert(
                                user.email,
                                flight_info,
                                last_price_record.price,
                                new_price
                            )

                # Record the new price
                new_price_record = PriceRecord(flight_id=flight.id, price=new_price)
                db.session.add(new_price_record)
                db.session.commit()

def start_scheduler():
    scheduler.add_job(check_flight_prices, 'interval', hours=24)
    scheduler.start()

def stop_scheduler():
    scheduler.shutdown()