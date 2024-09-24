# Flight Price Tracker

## Setup

1. Install Docker and Docker Compose.
2. Build and start the Docker containers:
   ```sh
   docker-compose up --build
   ```

## API Endpoints

### Create User

- **URL**: `/users`
- **Method**: `POST`
- **Data Params**: `{ "email": "user@example.com" }`
- **Success Response**:
  - **Code**: 201
  - **Content**: `{ "id": "user_id", "email": "user@example.com" }`

### Create Flight

- **URL**: `/flights`
- **Method**: `POST`
- **Data Params**: `{ "origin": "NYC", "destination": "LAX", "departure_date": "2024-12-01", "return_date": "2024-12-10" }`
- **Success Response**:
  - **Code**: 201
  - **Content**: `{ "id": "flight_id" }`

### Create Price Record

- **URL**: `/price_records`
- **Method**: `POST`
- **Data Params**: `{ "flight_id": "flight_id", "price": 199.99 }`
- **Success Response**:
  - **Code**: 201
  - **Content**: `{ "id": "price_record_id" }`
