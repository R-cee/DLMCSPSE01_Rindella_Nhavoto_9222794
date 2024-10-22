Event Management System
Project Overview

The Event Management System is a web application that allows users to explore, manage, and organize events. The platform caters to three types of users: Admins, Event Hosts, and Attendees, each with specific roles and capabilities.

    Attendees can browse events, like events, purchase tickets, and receive notifications for upcoming events.
    Event Hosts can submit their profiles for vetting, publish events, and view reports on ticket sales.
    Admins manage users and events, approve/reject profiles, and view logs.

Project Structure

    Backend: Flask (Python) with MySQL as the database.
    Frontend: React (JavaScript) for the user interface.
    Payment: Integrated with Stripe for payment processing.

Features
Admin:

    Manage users and events.
    Vetting process for event hosts (approval/rejection).
    Event management with approval/rejection workflow.
    View logs of user activities.
    Notifications and profile management.
    Admin creation

Event Hosts:

    Profile submission for vetting.
    Event creation and management.
    View sales reports and event statistics.

Attendees:

    Browse events by location, category, and country.
    Purchase tickets for events.
    Like/unlike events.
    View proof of payments and notifications for upcoming events.

Technologies Used
Backend:

    Flask: Handles routing, API logic, and database operations.
    MySQL: For managing user data, events, transactions, notifications, user interactions, likes, payment accounts, and profiles.
    Flask JWT: For handling user authentication and authorization.
    Stripe: For payment processing and refunds.

Frontend:

    React: Provides a dynamic and interactive user interface.
    React Router: For handling different routes and navigation.
    CSS: For styling components.

Database:

    MySQL: Tables include Users, Events, Profiles, Transactions, Likes, Notifications, Payment Accounts, etc.

Setup Instructions
Prerequisites

Ensure you have the following installed:

    Python 3.x
    MySQL
    Node.js & npm (for React)
    Stripe Account (for payment integration)
    React: ^17.0.0
    React Router: ^6.26.1
    Chart.js: ^3.0.0
    Stripe: For payment processing
    FontAwesome: For icons

Backend Setup
Clone the repository:

git clone https://github.com/R-cee/DLMCSPSE01_Rindella_Nhavoto_9222794.git
cd events-system-backend

Install dependencies:

pip install -r requirements.txt

Configure the MySQL Database: Update the config.py file with your MySQL credentials and run the following to create the database:

python

from app import create_database_if_not_exists
create_database_if_not_exists()

Run Flask application:

    flask run

Frontend Setup

    Navigate to the frontend directory:

cd ../events-system-frontend

Install dependencies:

npm install

Start the React development server:

sql

    npm start

Running the Full Application

After completing the setup, you should have both the Flask backend and the React frontend running:

    Flask backend runs on http://127.0.0.1:5000.
    React frontend runs on http://localhost:3000.

Important Endpoints
Backend (Flask)

    /register: Register new users.
    /login: User login, generates JWT.
    /host-dashboard: Displays event host dashboard.
    /landing: Displays attendee dashboard
    /vetting: Displays vetting form for new hosts.
    /create-event: Event creation endpoint.
    /admin-dashboard: Admin dashboard for managing events and profiles.
    /notifications: Fetch notifications for the user.
    /checkout: Handles payment with Stripe.
    /api/my-events: Displays events liked or purchased by attendees.

Frontend (React)

    /host-dashboard: Event host's dashboard.
    /admin-dashboard: Admin dashboard.
    /landing: Attendee dashboard.
    /vetting: Vetting form for new hosts.
    /events: Browse and filter events.

Testing

Run tests for both the backend and frontend:

    Backend (Flask): Use pytest or unittest to test API endpoints.
    Frontend (React): Use Jest and React Testing Library for component testing.

Payment Integration

    The system uses Stripe for processing event payments. Make sure to configure your Stripe secret key in the Flask backend (stripe.api_key in app.py).

This project is designed to facilitate event management for both hosts and attendees, with an admin panel for overseeing operations.
