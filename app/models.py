from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    email = db.Column(db.String(120), unique=True, nullable=False)
    flight_preferences = db.relationship('FlightPreference', back_populates='user')
    
class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    origin = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
    flight_preferences = db.relationship('FlightPreference', back_populates='flight')
    
class FlightPreference(db.Model):
    __tablename__ = 'flight_preferences'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    flight_id = db.Column(UUID(as_uuid=True), db.ForeignKey('flights.id'), nullable=False)
    user = db.relationship('User', back_populates='flight_preferences')
    flight = db.relationship('Flight', back_populates='flight_preferences')
    
class PriceRecord(db.Model):
    __tablename__ = 'price_records'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    flight_id = db.Column(UUID(as_uuid=True), db.ForeignKey('flights.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.now())
    flight = db.relationship('Flight', back_populates='price_records')
    
    