from flask import request, jsonify
from app import app, db
from app.models import User, Flight, FlightPreference, PriceRecord
import uuid

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
    return jsonify({'id': str(new_flight.id)}), 201

@app.route('/price_records', methods=['POST'])
def create_price_record():
    data = request.get_json()
    flight = Flight.query.get(data['flight_id'])
    if not flight:
        return jsonify({'error': 'Flight not found'}), 404
    new_price_record = PriceRecord(
        flight_id=data['flight_id'],
        price=data['price']
    )
    db.session.add(new_price_record)
    db.session.commit()
    return jsonify({'id': str(new_price_record.id)}), 201

@app.route('/preferences', methods=['POST'])
def create_preference():
    data = request.get_json()
    user = User.query.get(data['user_id'])
    flight = Flight.query.get(data['flight_id'])
    if not user or not flight:
        return jsonify({'error': 'User or Flight not found'}), 404
    new_preference = FlightPreference(user_id=user.id, flight_id=flight.id)
    db.session.add(new_preference)
    db.session.commit()
    return jsonify({'id': str(new_preference.id)}), 201

@app.route('/users/<user_id>/preferences', methods=['GET'])
def get_user_preferences(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    preferences = FlightPreference.query.filter_by(user_id=user.id).all()
    return jsonify([{
        'id': str(pref.id),
        'flight_id': str(pref.flight_id),
        'origin': pref.flight.origin,
        'destination': pref.flight.destination,
        'departure_date': pref.flight.departure_date.isoformat(),
        'return_date': pref.flight.return_date.isoformat() if pref.flight.return_date else None
    } for pref in preferences]), 200

@app.route('/preferences/<preference_id>', methods=['DELETE'])
def delete_preference(preference_id):
    preference = FlightPreference.query.get(preference_id)
    if not preference:
        return jsonify({'error': 'Preference not found'}), 404
    db.session.delete(preference)
    db.session.commit()
    return '', 204