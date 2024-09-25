import unittest
from app import app, db
from app.models import User, Flight, PriceRecord
from unittest.mock import patch

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

    def test_create_preference(self):
        user_response = self.app.post('/users', json={'email': 'test@example.com'})
        user_id = user_response.get_json()['id']
        flight_response = self.app.post('/flights', json={
            'origin': 'NYC',
            'destination': 'LAX',
            'departure_date': '2024-12-01',
            'return_date': '2024-12-08'
        })
        flight_id = flight_response.get_json()['id']
        response = self.app.post('/preferences', json={
            'user_id': user_id,
            'flight_id': flight_id
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.get_json())

    def test_get_user_preferences(self):
        user_response = self.app.post('/users', json={'email': 'test@example.com'})
        user_id = user_response.get_json()['id']
        flight_response = self.app.post('/flights', json={
            'origin': 'NYC',
            'destination': 'LAX',
            'departure_date': '2024-12-01',
            'return_date': '2024-12-08'
        })
        flight_id = flight_response.get_json()['id']
        self.app.post('/preferences', json={
            'user_id': user_id,
            'flight_id': flight_id
        })
        response = self.app.get(f'/users/{user_id}/preferences')
        self.assertEqual(response.status_code, 200)
        preferences = response.get_json()
        self.assertEqual(len(preferences), 1)
        self.assertEqual(preferences[0]['flight_id'], flight_id)

    def test_delete_preference(self):
        user_response = self.app.post('/users', json={'email': 'test@example.com'})
        user_id = user_response.get_json()['id']
        flight_response = self.app.post('/flights', json={
            'origin': 'NYC',
            'destination': 'LAX',
            'departure_date': '2024-12-01',
            'return_date': '2024-12-08'
        })
        flight_id = flight_response.get_json()['id']
        preference_response = self.app.post('/preferences', json={
            'user_id': user_id,
            'flight_id': flight_id
        })
        preference_id = preference_response.get_json()['id']
        response = self.app.delete(f'/preferences/{preference_id}')
        self.assertEqual(response.status_code, 204)
        # Verify the preference was deleted
        response = self.app.get(f'/users/{user_id}/preferences')
        self.assertEqual(len(response.get_json()), 0)
        
    @patch('app.services.amadeus_client.AmadeusClient.search_flights')
    def test_search_flights(self, mock_search_flights):
        mock_search_flights.return_value = [{'id': 'flight1', 'price': {'total': '100.00'}}]
        response = self.app.post('/search_flights', json={
            'origin': 'NYC',
            'destination': 'LAX',
            'departure_date': '2024-12-01',
            'return_date': '2024-12-08'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('flight1', str(response.get_json()))

if __name__ == '__main__':
    unittest.main()