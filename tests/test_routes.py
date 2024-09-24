import unittest
from app import app, db
from app.models import User, Flight, PriceRecord

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user(self):
        response = self.app.post('/users', json={'email': 'test@example.com'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.get_json())

    def test_create_flight(self):
        response = self.app.post('/flights', json={
            'origin': 'NYC',
            'destination': 'LAX',
            'departure_date': '2024-12-01',
            'return_date': '2024-12-08'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.get_json())

    def test_create_price_record(self):
        flight_response = self.app.post('/flights', json={
            'origin': 'NYC',
            'destination': 'LAX',
            'departure_date': '2024-12-01',
            'return_date': '2024-12-08'
        })
        self.assertEqual(flight_response.status_code, 201)
        flight_id = flight_response.get_json()['id']
        response = self.app.post('/price_records', json={
            'flight_id': flight_id,
            'price': 199.99
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.get_json())

if __name__ == '__main__':
    unittest.main()