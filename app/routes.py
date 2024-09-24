from flask import request, jsonify
from app import app, db
from app.models import User, Flight, FlightPreference, PriceRecord

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'email': new_user.email}), 201

@app.route('/flights', methods=['POST'])
def create_flight():
    data = request.get_json()
    new_flight = Flight(
        origin=data['origin'],
        destination=data['destination'],
        departure_date=data['departure_date'],
        return_date=data.get('return_date')
    )
    db.session.add(new_flight)
    db.session.commit()
    return jsonify({'id': new_flight.id}), 201

@app.route('/price_records', methods=['POST'])
def create_price_record():
    data = request.get_json()
    new_price_record = PriceRecord(
        flight_id=data['flight_id'],
        price=data['price']
    )
    db.session.add(new_price_record)
    db.session.commit()
    return jsonify({'id': new_price_record.id}), 201