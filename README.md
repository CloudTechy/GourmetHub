# GourmetHub

Connecting food lovers with local gourmet vendors.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies](#technologies)
- [API Endpoints](#api-endpoints)
- [Data Model](#data-model)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

GourmetHub is a web application designed to connect food enthusiasts with local gourmet vendors. Users can browse and search for vendors, view detailed information about them, and leave reviews. Vendors can manage their profiles, add food items, and handle orders efficiently.

## Features

- User registration and authentication
- Browse and search for gourmet vendors
- Vendor detail pages with food item listings
- User reviews and ratings for vendors
- Vendor management of food items and orders

## Technologies

- **Frontend:** React
- **Backend:** Node.js or Python
- **Database:** PostgreSQL (or another SQL-based database)
- **Authentication:** JWT
- **Styling:** CSS/SCSS
- **APIs:** RESTful API design

## API Endpoints

### User

- `POST /api/v1/register`: Register a new user
- `POST /api/v1/login`: Authenticate a user and return a token
- `GET /api/v1/user`: Get user details (authenticated route)

### Vendor

- `POST /api/v1/vendors`: Create a new vendor profile (vendor role)
- `GET /api/v1/vendors`: Get a list of all vendors
- `GET /api/v1/vendors/:id`: Get details of a specific vendor
- `PUT /api/v1/vendors/:id`: Update vendor profile (vendor role)
- `DELETE /api/v1/vendors/:id`: Delete vendor profile (vendor role)

### Food Item

- `POST /api/v1/fooditems`: Add a new food item (vendor role)
- `GET /api/v1/fooditems`: Get a list of all food items
- `GET /api/v1/fooditems/:id`: Get details of a specific food item
- `PUT /api/v1/fooditems/:id`: Update food item details (vendor role)
- `DELETE /api/v1/fooditems/:id`: Delete food item (vendor role)

### Review

- `POST /api/v1/reviews`: Add a new review for a vendor (user role)
- `GET /api/v1/reviews/:vendorId`: Get all reviews for a vendor
- `PUT /api/v1/reviews/:id`: Update a review (user role)
- `DELETE /api/v1/reviews/:id`: Delete a review (user role)

### Order

- `POST /api/v1/orders`: Place a new order (user role)
- `GET /api/v1/orders`: Get all orders (vendor role)
- `GET /api/v1/orders/:id`: Get details of a specific order
- `PUT /api/v1/orders/:id`: Update order status (vendor role)
- `DELETE /api/v1/orders/:id`: Cancel an order (user role)

## Data Model

### User

- `id` (UUID)
- `username` (VARCHAR)
- `email` (VARCHAR)
- `password` (VARCHAR)
- `role` (VARCHAR) - [vendor, customer]
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

### Vendor

- `id` (UUID)
- `user_id` (UUID)
- `name` (VARCHAR)
- `description` (VARCHAR)
- `contact_details` (VARCHAR)
- `location` (VARCHAR)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

### FoodItem

- `id` (UUID)
- `vendor_id` (UUID)
- `name` (VARCHAR)
- `description` (VARCHAR)
- `price` (DECIMAL)
- `photo_url` (VARCHAR)
- `status` (VARCHAR) - [active, inactive]
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

### Review

- `id` (UUID)
- `vendor_id` (UUID)
- `user_id` (UUID)
- `rating` (INTEGER)
- `comment` (TEXT)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

### Order

- `id` (UUID)
- `user_id` (UUID)
- `vendor_id` (UUID)
- `total_price` (DECIMAL)
- `status` (VARCHAR) - [pending, confirmed, shipped, delivered, canceled]
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

### OrderItem

- `id` (UUID)
- `order_id` (UUID)
- `fooditem_id` (UUID)
- `quantity` (INTEGER)
- `price` (DECIMAL)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/gourmethub.git
   ```

2. Navigate to the project directory:

   ```bash
   cd gourmethub
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt  # For Python
   ```

4. Set up the database:

   ```bash
   # For PostgreSQL
   createdb gourmethub
   ```

5. Run the development server:
   ```bash
   python app.py  # For Python
   ```

## Usage

1. Open your browser and navigate to `http://localhost:5000` (or the appropriate port).
2. Register as a new user or log in with existing credentials.
3. Browse vendors, view details, leave reviews, and place orders.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for details on the code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
