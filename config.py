import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:pass@db:5432/flight-price-tracker'
    AMADEUS_API_KEY = 'E0GVI8qfcGgmDPZ92U0lAfDkGsGKHQKw'
    AMADEUS_API_SECRET = 'iwTGKop0N6nEe8WL'
    NOTIFICATION_SERVICE_URL = os.environ.get('NOTIFICATION_SERVICE_URL') or 'http://notification-service:5000'
