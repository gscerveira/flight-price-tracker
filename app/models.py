from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    email = db.column(db.String(120), unique=True, nullable=False)
    flight_preferences = db.relationship('FlightPreference', back_populates='user')