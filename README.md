# Flight Price Tracker

Flight Price Tracker is a web application that allows users to track flight prices and receive notifications when prices drop. It integrates with the Amadeus API for flight data and includes a notification service for alerting users about price changes.

## Setup Instructions

1. Install Docker and Docker Compose on your system if you haven't already.

2. Clone the repository to your local machine.

3. Create a `.env` file in the root directory of the project and add the following environment variables:

   ```
   AMADEUS_API_KEY=your_amadeus_api_key
   AMADEUS_API_SECRET=your_amadeus_api_secret
   NOTIFICATION_SERVICE_URL=http://notification-service:8000
   ```

   Replace `your_amadeus_api_key` and `your_amadeus_api_secret` with your actual Amadeus API credentials.

4. Build and start the Docker containers:

   ```sh
   docker-compose up --build
   ```

   This command will build the Docker images and start the containers for the web application, PostgreSQL database, and notification service.

5. Once the containers are up and running, you can access the application at `http://localhost:5000`.

6. To view the API documentation, navigate to `http://localhost:5000/apidocs/` in your web browser.

## API Endpoints

The Flight Price Tracker API provides the following endpoints:

- POST /users: Create a new user
- POST /flights: Create a new flight
- POST /price_records: Create a new price record
- POST /preferences: Create a new flight preference
- GET /users/{user_id}/preferences: Get user's flight preferences
- DELETE /preferences/{preference_id}: Delete a flight preference
- POST /search_flights: Search for flights

For detailed information on request and response formats, please refer to the Swagger documentation available at `/apidocs/` when the application is running.

## Development

To set up the development environment:

1. Create a Python virtual environment:

   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

2. Install the required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Set up the PostgreSQL database and update the `SQLALCHEMY_DATABASE_URI` in `config.py` if necessary.

4. Run database migrations:

   ```sh
   flask db upgrade
   ```

5. Start the development server:

   ```sh
   flask run
   ```

## Testing

To run the tests:

  ```sh
  python -m unittest discover tests/
  ```




