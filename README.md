# Calorie Counter Application README

## Overview

The Calorie Counter is a web and mobile-friendly application designed to help users track their daily food intake, monitor macronutrients, and manage calories efficiently. It allows users to log meals, view detailed nutritional breakdowns, and track progress over time. The app emphasizes simplicity, usability, and accurate tracking to support healthy dietary habits and weight management goals.

## Features

* **User Authentication**: Secure registration and login system to store personal profiles.
* **Food Logging**: Add meals, including portion sizes, calories, and macronutrient content.
* **Meal Categories**: Track breakfast, lunch, dinner, and snacks separately.
* **Nutrient Breakdown**: Display calories, proteins, carbohydrates, and fats for each meal and daily totals.
* **Progress Tracking**: View weekly and monthly summaries of caloric intake and trends.
* **Search Functionality**: Find foods from a database with nutritional information for accurate logging.
* **Custom Foods**: Add user-defined foods if not available in the database.
* **Mobile Compatibility**: Responsive design for use on smartphones, tablets, and desktops.

## Technologies Used

* **Backend**: Django REST Framework, PostgreSQL
* **Frontend**: React.js / React Native (depending on mobile or web version)
* **Authentication**: Token-based authentication with secure password hashing
* **Deployment**: Dockerized environment for development and production

## Installation

1. Clone the repository to your local machine.
2. Set up a Python virtual environment and activate it.
3. Install dependencies using `pip install -r requirements.txt`.
4. Configure the `.env` file with your database credentials and secret keys.
5. Run database migrations with `python manage.py migrate`.
6. Start the development server with `python manage.py runserver`.

For the frontend:

1. Navigate to the frontend directory.
2. Install dependencies with `npm install` or `yarn install`.
3. Start the frontend development server with `npm start` or `yarn start`.

## Usage

1. Register a user account and log in.
2. Add meals and input portion sizes.
3. Track daily nutritional intake and monitor trends via the dashboard.
4. Use the search feature to quickly find foods from the database.
5. Customize food entries for items not in the database.

## Future Improvements

* Integration with barcode scanning for faster food entry.
* Personalized calorie goals based on user weight, height, and activity level.
* Graphical visualization of macronutrient trends over time.
* Push notifications for meal reminders and hydration tracking.

## Contributing

Contributions are welcome. Please fork the repository, make your changes, and submit a pull request with clear descriptions. Ensure code quality, follow existing structure, and write meaningful commit messages.

