from amadeus import Client, ResponseError
from flask import current_app

class AmadeusClient:
    def __init__(self):
        self.client = Client(
            client_id=current_app.config['AMADEUS_API_KEY'],
            client_secret=current_app.config['AMADEUS_API_SECRET']
        )
        
    def search_flights(self, origin, destination, departure_date, return_date=None):
        try:
            response = self.client.shopping.flight_offers_search.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate=departure_date,
                returnDate=return_date,
                adults=1,
                max=5
            )
            return response.data
        except ResponseError as error:
            print(f"An error occurred: {error}")
            return None
        
    def get_flight_price(self, flight_offer):
        try:
            response = self.client.shopping.flight_offers.pricing.post(flight_offer)
            return response.data['flightOffers'][0]['price']['total']
        except ResponseError as error:
            print(f"An error occurred: {error}")
            return None