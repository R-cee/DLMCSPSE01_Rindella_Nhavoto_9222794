Event Management System
Project Overview

The Event Management System is a web application for exploring, managing, and organizing events. The platform is designed for three types of users:

    Attendees: Browse, like, purchase tickets, and receive notifications for events.
    Event Hosts: Submit profiles for vetting, publish events, and view ticket sales reports.
    Admins: Manage users/events, approve/reject profiles, and view activity logs.

Project Structure

    Backend: Flask (Python) with MySQL as the database.
    Frontend: React (JavaScript) for the user interface.
    Payment: Integrated with Stripe for payment processing.

Features
Admin

    Manage users and events
    Vetting process for event hosts (approval/rejection)
    Event approval/rejection workflow
    User activity logs
    Notifications and profile management

Event Hosts

    Profile submission for vetting
    Event creation and management
    Sales reports and event statistics

Attendees

    Event browsing by location, category, and country
    Ticket purchasing
    Like/unlike events
    Notifications for upcoming events

Technologies Used

Backend: Flask, MySQL, Flask JWT, Stripe
Frontend: React, React Router, CSS
Database: MySQL with tables for Users, Events, Profiles, Transactions, Likes, Notifications, Payment Accounts, etc.
Setup Instructions
Prerequisites

    Python 3.x
    MySQL
    Node.js & npm
    Stripe account (for payment integration)
    Dependencies:
        React: ^17.0.0
        React Router: ^6.26.1
        Chart.js: ^3.0.0
        FontAwesome: For icons

Backend Setup

    Clone the repository:

git clone -b master https://github.com/R-cee/DLMCSPSE01_Rindella_Nhavoto_9222794.git
cd events-system-backend

Install dependencies:

pip install -r requirements.txt

Database Configuration:

    Update config.py with your MySQL credentials.
    Run:

    from app import create_database_if_not_exists
    create_database_if_not_exists()

Run Flask Application:

    flask run

Frontend Setup

    Navigate to frontend directory:

cd ../events-system-frontend

Install dependencies:

npm install

Start React development server:

    npm start

Running the Full Application

    Flask backend runs on http://127.0.0.1:5000
    React frontend runs on http://localhost:3000

Important Endpoints
Backend (Flask)

    /register: Register new users
    /login: User login, generates JWT
    /host-dashboard: Event host dashboard
    /landing: Attendee dashboard
    /vetting: Vetting form for new hosts
    /create-event: Event creation endpoint
    /admin-dashboard: Admin dashboard
    /notifications: User notifications
    /checkout: Stripe payment processing
    /api/my-events: Display liked or purchased events

Frontend (React)

    /host-dashboard: Event host dashboard
    /admin-dashboard: Admin dashboard
    /landing: Attendee dashboard
    /vetting: Vetting form for new hosts
    /events: Event browsing and filtering

Testing

    Backend: Use pytest or unittest
    Frontend: Use Jest and React Testing Library

Payment Integration

    Stripe is used for payments. Configure your Stripe secret key in the Flask backend (stripe.api_key in app.py).

AWS EC2 Configuration Instructions

For deployment on AWS EC2:

    Launch EC2 Instance:
        Install Python, Node.js, and MySQL on the instance.
        Open necessary ports (5000 for Flask, 3000 for React, and 3306 for MySQL if accessing externally) in the security group.

    Database Setup on EC2:
        Ensure MySQL is running and accessible.
        Run create_database_if_not_exists() to initialize the database.

    Update Paths in config.py:
        Set UPLOAD_EVENT, UPLOAD_ID, and UPLOAD_CERT with absolute paths on EC2, e.g., /home/ec2-user/events-system-backend/event_images.

    Start Services:
        Run flask run for the backend.
        Start the frontend server with npm start.

Docker Configuration

To simplify local development:

    Add a docker-compose.yml file for the backend, frontend, and MySQL services.

    Run Docker:

docker-compose up

Access:

    Backend at http://localhost:5000
    Frontend at http://localhost:3000
