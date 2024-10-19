import os, pymysql
from models import db, User, UserInteraction, Event, Transaction, Notification, Like
from flask import Flask, jsonify, request, redirect, url_for, send_from_directory
from flask_login import LoginManager, logout_user
from datetime import timedelta, datetime
from flask_cors import CORS
from config import Config
from flask import request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import stripe

app = Flask(__name__, static_folder='../events-system-frontend/build', static_url_path='')
CORS(app)

stripe.api_key = 'sk_test_51Q9xXHP5Lv2xb3IZKkyE6Dhh9WuVKx30sTt9b83BlgXL4THFKbbWCVIRJ1JaeHxk0J46oEArSxZGnYK45HbG69yw0072XMGkWh'

app.config.from_object(Config)
app.config['JWT_SECRET_KEY'] = Config.SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)

db.init_app(app)

def create_database_if_not_exists():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='P@ssw0rd24')
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS `events-system-db`;")
    cursor.close()
    connection.close()

def notify_upcoming_events_for_user(user_id):
    """
    Function to check for upcoming events liked or paid for by the user.
    It creates notifications if any event is approaching within 1-2 days.
    """
    try:
        now = datetime.utcnow()
        one_day_from_now = now + timedelta(days=1)
        two_days_from_now = now + timedelta(days=2)

        print(f"Current UTC time: {now}")
        print(f"Checking events between {one_day_from_now} and {two_days_from_now}")

        upcoming_paid_events = db.session.query(Event).join(Transaction, Transaction.event_id == Event.event_id)\
            .filter(Transaction.user_id == user_id, Event.event_date.between(one_day_from_now, two_days_from_now))\
            .all()

        upcoming_liked_events = db.session.query(Event).join(Like, Like.event_id == Event.event_id)\
            .filter(Like.user_id == user_id, Event.event_date.between(one_day_from_now, two_days_from_now))\
            .all()

        upcoming_events = set(upcoming_paid_events + upcoming_liked_events)

        print(f"Found upcoming events: {upcoming_events}")

        for event in upcoming_events:
            notification_message = f"{event.event_name} is approaching on {event.event_date.strftime('%Y-%m-%d %H:%M')}"
            new_notification = Notification(
                user_id=user_id,
                message=notification_message,
                is_read=False,
                created_at=datetime.utcnow()
            )
            db.session.add(new_notification)

        db.session.commit()

    except Exception as e:
        print(f"Failed to create notifications for user {user_id}: {str(e)}")

# Function to create admin user if not exists
def create_admin_user():
    admin_username = "admin"
    admin_email = "admin@example.com"
    admin_password = "admin123"

    existing_admin = User.query.filter_by(username=admin_username).first()

    if not existing_admin:
        admin_user = User(
            username=admin_username,
            email=admin_email,
            role="Admin"
        )
        admin_user.set_password(admin_password)
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created!")
    else:
        print("Admin user already exists.")

with app.app_context():
    create_database_if_not_exists() 
    db.create_all()
    create_admin_user()  

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """
    Display the static files from the frontend build directory.
    If a path is provided and the file exists, it serves that file.
    Otherwise, it serves the index.html file for React routing.
    """
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

class UserRoutes:
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """
        Register a new user.
        GET: Display the registration page.
        POST: Create a new user in the database after validating the input.
        """
        if request.method == 'GET':
            return send_from_directory(app.static_folder, 'index.html')  # Serve the React app
        
        form_data = request.json
        errors = {}

        if not form_data.get('username'):
            errors['username'] = 'Username is required'
        if not form_data.get('email'):
            errors['email'] = 'Email is required'
        if not form_data.get('password'):
            errors['password'] = 'Password is required'
        if not form_data.get('role'):
            errors['role'] = 'Role is required'

        if errors:
            return jsonify({'errors': errors}), 400

        if User.query.filter_by(username=form_data['username']).first():
            errors['username'] = 'Username already exists'
        if User.query.filter_by(email=form_data['email']).first():
            errors['email'] = 'Email already exists'

        if errors:
            return jsonify({'errors': errors}), 400

        user = User(
            username=form_data['username'],
            email=form_data['email'],
            role=form_data['role']
        )
        user.set_password(form_data['password'])
        db.session.add(user)
        db.session.commit()
    
        return jsonify({'message': 'User registered successfully'}), 200

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """
        Login an existing user.
        GET: Serve the login page.
        POST: Authenticate user and generate JWT if successful.
        """
        if request.method == 'GET':
            return send_from_directory(app.static_folder, 'index.html')

        form_data = request.get_json()

        if not form_data:
            return jsonify({'errors': 'Invalid data provided'}), 400

        user = User.query.filter_by(username=form_data['username']).first()

        if user and user.check_password(form_data['password']):
            if user.status != 'active':
                return jsonify({'errors': 'User is not active'}), 400

            access_token = create_access_token(identity={
                'user_id': user.user_id,
                'username': user.username,
                'role': user.role
            })
            
            if user.role == 'Attendee':
                redirect_url = '/landing'
            elif user.role == 'EventHost':
                redirect_url = '/host-dashboard'
            elif user.role == 'Admin':
                redirect_url = '/admin-dashboard'
            else:
                return jsonify({'errors': 'Invalid user role'}), 400

            return jsonify({
                'access_token': access_token,
                'redirect': redirect_url,
                'username': user.username,
                'role': user.role
            }), 200
        else:
            return jsonify({'errors': 'Invalid username or password'}), 400

    @staticmethod
    @app.route('/logout')
    def logout():
        """
        Logout the current user by removing their session.
        Redirects to the login page.
        """
        logout_user()
        return redirect(url_for('login'))

    def allowed_file(filename):
            """
            Check if the provided filename has an allowed file extension.
            Returns True if the file extension is allowed, otherwise False.
            """
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    @app.route('/uploads/ids/<filename>')
    def uploaded_id_file(filename):
        """
        Display the government ID document image.
        """
        return send_from_directory(app.config['UPLOAD_ID'], filename)

    @app.route('/uploads/certs/<filename>')
    def uploaded_cert_file(filename):
        """
        Display the business certificate image.
        """
        return send_from_directory(app.config['UPLOAD_CERT'], filename)
      
    @app.route('/event_images/<filename>')
    def event_images(filename):
        return send_from_directory(app.config['UPLOAD_EVENT'], filename)
  
    @app.route('/landing')
    def landing():
        """
        Display the landing page of the Attendee.
        """
        return send_from_directory(app.static_folder, 'index.html')
    
    @app.route('/events/countries', methods=['GET'])
    def get_countries():
        """
        Retrieve the list of distinct countries from the events table.
        Returns a JSON list of country names.
        """
        countries = db.session.query(Event.event_country).distinct().all()
        country_list = [country[0] for country in countries]
        return jsonify(country_list)

    @app.route('/events/filters', methods=['GET'])
    def get_filters():
        """
        Get event filters based on the selected country.
        Returns the locations and categories available for the specified country.
        """
        country = request.args.get('country')

        if not country:
            return jsonify({'error': 'Country is required'}), 400

        locations = db.session.query(Event.event_location).filter(Event.event_country == country).distinct().all()
        categories = db.session.query(Event.event_category).filter(Event.event_country == country).distinct().all()

        location_list = [location[0] for location in locations]
        category_list = [category[0] for category in categories]

        return jsonify({
            'locations': location_list,
            'categories': category_list
        })

    @app.route('/events', methods=['GET'])
    def get_events():
        """
        Retrieve a list of events filtered by country, location, category, and status.
        Default status is 'Approved'.
        """
        country = request.args.get('country')
        location = request.args.get('location')
        category = request.args.get('category')
        status = request.args.get('status', 'Approved') 

        if not country:
            return jsonify({'error': 'Country is required'}), 400

        query = Event.query.filter_by(event_country=country, event_status=status)

        if location:
            query = query.filter_by(event_location=location)

        if category:
            query = query.filter_by(event_category=category)

        events = query.all()
        events_data = [
            {
                'event_id': event.event_id,
                'event_name': event.event_name,
                'event_description': event.event_description,
                'event_location': event.event_location,
                'event_category': event.event_category,
                'event_date': event.event_date.strftime('%Y-%m-%dT%H:%M'),
                'event_price': event.event_price,
                'event_capacity': event.event_capacity,
                'event_status': event.event_status,
                'event_poster': event.event_poster
            }
            for event in events
        ]

        return jsonify(events_data)

    @app.route('/api/events/<int:event_id>', methods=['GET'])
    def get_event_details(event_id):
        """
        Retrieve the details of a specific event by its event ID.
        Returns the event data in JSON format.
        """
        event = Event.query.get(event_id)
        if not event:
            return jsonify({'error': 'Event not found'}), 404

        event_data = {
            'event_id': event.event_id,
            'event_name': event.event_name,
            'event_description': event.event_description,
            'event_location': event.event_location,
            'event_date': event.event_date.strftime('%Y-%m-%dT%H:%M'),
            'event_price': event.event_price,
            'event_capacity': event.event_capacity,
            'event_poster': event.event_poster,
            'event_status': event.event_status
        }

        return jsonify(event_data)

    @app.route('/create-payment-intent', methods=['POST'])
    @jwt_required()
    def create_payment_intent():
        try:
            data = request.json
            amount = data.get('amount') 

            intent = stripe.PaymentIntent.create(
                amount=int(amount),
                currency='usd',
                automatic_payment_methods={'enabled': True},
            )

            return jsonify({'clientSecret': intent['client_secret']}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/checkout', methods=['POST'])
    @jwt_required()
    def checkout():
        try:
            current_user = get_jwt_identity()
            data = request.json
            payment_intent_id = data.get('payment_intent_id')
            event_id = data.get('event_id')
            tickets_purchased = data.get('tickets_purchased', 1)

            if not payment_intent_id or not event_id:
                return jsonify({'error': 'Missing payment intent ID or event ID'}), 400

            intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            if intent['status'] == 'succeeded':
                amount_paid = intent['amount'] / 100 
                
    
                event = Event.query.get(event_id)
                if not event:
                    return jsonify({'error': 'Event not found'}), 404

                if event.event_capacity < tickets_purchased:
                    return jsonify({'error': 'Not enough tickets available'}), 400

                new_transaction = Transaction(
                    event_id=event_id,
                    user_id=current_user.get('user_id'),
                    payment_status='Success',
                    amount_paid=amount_paid,
                    quantity=tickets_purchased,
                    transaction_date=datetime.utcnow()
                )

                event.event_capacity -= tickets_purchased

                db.session.add(new_transaction)
                db.session.commit()

                return jsonify({'message': 'Payment recorded successfully'}), 200
            else:
                return jsonify({'error': 'Payment not completed'}), 400

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to complete payment: {str(e)}'}), 500

    @app.route('/events/<int:event_id>/like', methods=['POST', 'DELETE'])
    @jwt_required()
    def like_unlike_event(event_id):
        """
        Handle the like/unlike event action by a user.
        This endpoint stores likes in the 'Like' table.
        """
        try:
            current_user = get_jwt_identity()
            user_id = current_user.get('user_id')

            # Handle 'like' action
            if request.method == 'POST':
                existing_like = Like.query.filter_by(user_id=user_id, event_id=event_id).first()
                if existing_like:
                    return jsonify({'message': 'User has already liked this event'}), 200  # Already liked

                new_like = Like(user_id=user_id, event_id=event_id)
                db.session.add(new_like)
                db.session.commit()
                return jsonify({'message': 'Event liked successfully'}), 200

            # Handle 'unlike' action
            elif request.method == 'DELETE':
                existing_like = Like.query.filter_by(user_id=user_id, event_id=event_id).first()
                if existing_like:
                    db.session.delete(existing_like)
                    db.session.commit()
                    return jsonify({'message': 'Event unliked successfully'}), 200
                else:
                    return jsonify({'message': 'Like not found'}), 404

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to like/unlike event', 'details': str(e)}), 500

    @app.route('/api/my-events', methods=['GET'])
    @jwt_required()
    def get_my_events():
        """
        Get a list of events purchased and liked by the current user.
        Requires user authentication (JWT).
        """
        try:
            current_user = get_jwt_identity()
            user_id = current_user.get('user_id')

            # Get events purchased by the user
            purchased_events = db.session.query(Event).join(Transaction).filter(Transaction.user_id == user_id).all()

            # Get events liked by the user
            liked_events = db.session.query(Event).join(Like).filter(Like.user_id == user_id).all()

            purchased_events_data = [
                {
                    'event_id': event.event_id,
                    'event_name': event.event_name,
                    'event_date': event.event_date,
                    'event_location': event.event_location,
                    'event_poster': event.event_poster,
                    'event_category': event.event_category,
                }
                for event in purchased_events
            ]

            liked_events_data = [
                {
                    'event_id': event.event_id,
                    'event_name': event.event_name,
                    'event_date': event.event_date,
                    'event_location': event.event_location,
                    'event_poster': event.event_poster,
                    'event_category': event.event_category,
                }
                for event in liked_events
            ]

            return jsonify({
                'purchased_events': purchased_events_data,
                'liked_events': liked_events_data
            }), 200

        except Exception as e:
            return jsonify({'error': 'Failed to retrieve events'}), 500
          
    @app.route('/view-proof-of-payment', methods=['GET'])
    @jwt_required()
    def view_proof_of_payment():
        """
        Display the proof of payment page.
        Requires user authentication (JWT).
        """
        try:
            current_user = get_jwt_identity()
            user_id = current_user.get('user_id')

            transactions = db.session.query(Transaction, Event).join(Event, Transaction.event_id == Event.event_id).filter(Transaction.user_id == user_id).all()

            transactions_data = [
                {
                    'transaction_id': transaction.Transaction.transaction_id,
                    'event_name': transaction.Event.event_name,
                    'amount_paid': transaction.Transaction.amount_paid,
                    'payment_status': transaction.Transaction.payment_status,
                    'transaction_date': transaction.Transaction.transaction_date,
                    'quantity': transaction.Transaction.quantity
                }
                for transaction in transactions
            ]

            return jsonify({'transactions': transactions_data}), 200
        except Exception as e:
            return jsonify({'error': 'Failed to retrieve transactions'}), 500
    
    @app.route('/attendee-notifications', methods=['GET'])
    @jwt_required()
    def get_notifications():
        current_user = get_jwt_identity()
        user_id = current_user.get('user_id')

        notify_upcoming_events_for_user(user_id)

        notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()

        notifications_data = [
            {
                'message': notification.message,
                'is_read': notification.is_read,
                'created_at': notification.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            for notification in notifications
        ]

        return jsonify({'notifications': notifications_data}), 200

    @app.route('/notifications/mark-as-read', methods=['POST'])
    @jwt_required()
    def mark_notifications_as_read():
        """
        Marks all unread notifications for the current user as read.
        """
        try:
            current_user = get_jwt_identity()
            user_id = current_user.get('user_id')

            Notification.query.filter_by(user_id=user_id, is_read=False).update({'is_read': True})
            db.session.commit()

            return jsonify({'message': 'Notifications marked as read successfully'}), 200

        except Exception as e:
            return jsonify({'error': f'Failed to mark notifications as read: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
