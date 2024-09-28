import requests
from flask import current_app

class NotificationService:
    def __init__(self):
        self.base_url = current_app.config['NOTIFICATION_SERVICE_URL']

    def send_price_drop_alert(self, user_email, flight_info, old_price, new_price):
        endpoint = f"{self.base_url}/notifications/price-drop"
        payload = {
            "user_email": user_email,
            "flight_info": flight_info,
            "old_price": old_price,
            "new_price": new_price
        }
        try:
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            current_app.logger.error(f"Failed to send price drop alert: {str(e)}")
            return False