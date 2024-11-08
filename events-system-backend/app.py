import os, pymysql
from models import db, User, UserInteraction, Event, Transaction, Profile ,AdminDetails, Notification, Like, Transaction, PaymentAccount
from flask import Flask, jsonify, request, redirect, url_for, send_from_directory
from flask_login import LoginManager, logout_user, current_user
from datetime import timedelta, datetime, datetime, datetime
from flask_cors import CORS
from config import Config
from werkzeug.utils import secure_filename
from flask import request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import stripe
from sqlalchemy.exc import IntegrityError

app = Flask(__name__, static_folder='../events-system-frontend/build', static_url_path='')
CORS(app)

stripe.api_key = Config.STRIPE_SECRET_KEY

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

def notify_upcoming_events_for_user(user_id):
    """
    Function to check for upcoming events liked or paid for by the user.
    It creates notifications if any event is approaching within 1-2 days.
    """
    try:
        today = datetime.utcnow()
        two_days_later = today + timedelta(days=2)

        events = db.session.query(Event).join(Transaction, Transaction.event_id == Event.event_id)\
            .filter(Transaction.user_id == user_id, Event.event_date.between(today, two_days_later))\
            .all()

        liked_events = db.session.query(Event).join(Like, Like.event_id == Event.event_id)\
            .filter(Like.user_id == user_id, Event.event_date.between(today, two_days_later))\
            .all()

        upcoming_events = set(events + liked_events)

        for event in upcoming_events:
            existing_notification = Notification.query.filter_by(
                user_id=user_id, 
                message=f"{event.event_name} is approaching on {event.event_date.strftime('%Y-%m-%d %H:%M')}"
            ).first()

            if not existing_notification:
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
        print(f"Failed to create upcoming event notifications for user {user_id}: {str(e)}")

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
            , 'username': user.username})


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

    @app.route('/event_images/<filename>')
    def event_images(filename):
        file_path = os.path.join(app.config['UPLOAD_EVENT'], filename)
        print(f"Serving file from: {file_path}")
        return send_from_directory(app.config['UPLOAD_EVENT'], filename)

    @app.route('/uploads/certs/<filename>')
    def uploaded_cert_file(filename):
        """
        Display the business certificate image.
        """
        return send_from_directory(app.config['UPLOAD_CERT'], filename)
      
    @app.route('/api/profile-status')
    @jwt_required()
    def get_profile_status():
        """
        Get the status of the current user's profile.
        Requires user authentication (JWT).
        """
        current_user = get_jwt_identity()
        
        user_id = current_user.get('user_id')
        profile = Profile.query.filter_by(user_id=user_id).first()
        if profile:
            return jsonify({'status': profile.status})
        return jsonify({'status': None})
    
    @app.route('/host-dashboard')
    def host_dashboard():
        """
        Display the host dashboard page.
        """
        return send_from_directory(app.static_folder, 'index.html')
   
    @app.route('/vetting', methods=['GET','POST'])
    @jwt_required()
    def vetting():
        """
        Submit vetting form data.
        Requires user authentication (JWT).
        """
        current_user = get_jwt_identity()
        
        user_id = current_user.get('user_id')
        
        if request.method == 'GET':
            existing_profile = Profile.query.filter_by(user_id=user_id).first()
            if existing_profile:
                return jsonify({'error': 'Profile already submitted and pending approval'}), 403

            return jsonify({
                'first_name': '',
                'last_name': '',
                'phone_number': '',
                'address': '',
                'host_type': 'Individual',
                'document_id': None,
                'business_certificate': None
            }), 200
        
        if request.method == 'POST':
            existing_profile = Profile.query.filter_by(user_id=user_id).first()
            if existing_profile:
                return jsonify({'error': 'Profile already submitted and pending approval'}), 403

            form_data = request.form
            files = request.files

            document_id_file = files.get('document_id')
            business_certificate_file = files.get('business_certificate') if form_data.get('host_type') in ['Business', 'Organization'] else None

            document_id_filename = None
            business_certificate_filename = None

            if document_id_file:
                document_id_filename = secure_filename(document_id_file.filename)
                document_id_file.save(os.path.join(app.config['UPLOAD_ID'], document_id_filename))

            if business_certificate_file:
                business_certificate_filename = secure_filename(business_certificate_file.filename)
                business_certificate_file.save(os.path.join(app.config['UPLOAD_CERT'], business_certificate_filename))

            profile = Profile(
                user_id=user_id,
                first_name=form_data.get('first_name'),
                last_name=form_data.get('last_name'),
                phone_number=form_data.get('phone_number'),
                address=form_data.get('address'),
                host_type=form_data.get('host_type'),
                document_id=document_id_filename,
                business_certificate=business_certificate_filename,
                status='Pending' 
            )
            
            db.session.add(profile)
            db.session.commit()
            
            log = UserInteraction(user_id=current_user.get('user_id'), username=current_user.get('username'), action='Profile_submitted')
            db.session.add(log)
            db.session.commit()

            return jsonify({'message': 'Profile submitted and pending approval'}), 200

    @app.route('/create-event', methods=['POST'])
    @jwt_required()
    def create_event():
        """
        Create a new event.
        Requires user authentication (JWT).
        """
        current_user = get_jwt_identity() 
        form_data = request.form
        files = request.files.getlist('event_poster')

        try:
            event_date = datetime.strptime(form_data['event_date'], '%Y-%m-%dT%H:%M')
        except ValueError:
            return jsonify({'errors': {'event_date': 'Invalid date format'}}), 400

        poster_filename = None
        if files:
            file = files[0]
            if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']:
                poster_filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_EVENT'], poster_filename)
                file.save(file_path)
            else:
                return jsonify({'errors': {'event_poster': 'Invalid file format'}}), 400

        new_event = Event(
            host_id=current_user.get('user_id'),
            event_name=form_data['event_name'],
            event_description=form_data['event_description'],
            event_category=form_data['event_category'],
            event_country=form_data['event_country'],
            event_location=form_data['event_location'],
            event_date=event_date,
            event_price=float(form_data['event_price']),
            event_capacity=int(form_data['event_capacity']),
            event_poster=poster_filename,
            event_status='Pending',
        )

        db.session.add(new_event)
        db.session.commit()

        log = UserInteraction(user_id=current_user.get('user_id'), username=current_user.get('username'), action='Event_created')
        db.session.add(log)
        db.session.commit()

        return jsonify({'message': 'Event created successfully'}), 200

    @app.route('/edit-event/<int:event_id>', methods=['GET'])
    @jwt_required()
    def edit_event(event_id):
        """
        Get the details of an existing event by its event ID.
        Returns the event data in JSON format.
        """
        event = Event.query.get(event_id)
        if event:
            event_data = {
                'event_id': event.event_id,
                'event_name': event.event_name,
                'event_description': event.event_description,
                'event_country': event.event_country,
                'event_location': event.event_location,
                'event_date': event.event_date.strftime('%Y-%m-%dT%H:%M'),
                'event_price': event.event_price,
                'event_capacity': event.event_capacity,
                'event_category': event.event_category,
                'event_poster': event.event_poster,
                'event_status': event.event_status
            }
            return jsonify(event_data)
        return jsonify({'error': 'Event not found'}), 404

    @app.route('/update-event/<int:event_id>', methods=['POST'])
    @jwt_required()
    def update_event(event_id):
        """
        Update an existing event.
        Only events with status 'Pending' can be updated.
        """
        current_user = get_jwt_identity()
        event = Event.query.get(event_id)

        if not event:
            return jsonify({'error': 'Event not found'}), 404

        if event.event_status != 'Pending':
            return jsonify({'error': 'Event cannot be edited'}), 403

        form_data = request.form
        files = request.files.getlist('event_poster')

        try:
            event.event_name = form_data.get('event_name', event.event_name)
            event.event_description = form_data.get('event_description', event.event_description)
            event.event_country = form_data.get('event_country', event.event_country)
            event.event_location = form_data.get('event_location', event.event_location)
            event.event_date = datetime.strptime(form_data['event_date'], '%Y-%m-%dT%H:%M')
            event.event_price = float(form_data.get('event_price', event.event_price))
            event.event_capacity = int(form_data.get('event_capacity', event.event_capacity))
            event.event_category = form_data.get('event_category', event.event_category)

            if files and files[0]:
                file = files[0]
                if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']:
                    poster_filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_EVENT'], poster_filename)
                    file.save(file_path)
                    event.event_poster = poster_filename

            db.session.commit()

            log = UserInteraction(user_id=current_user.get('user_id'), username=current_user.get('username'), action='Event_updated')
            db.session.add(log)
            db.session.commit()

            return jsonify({'message': 'Event updated successfully'}), 200

        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'error': 'Database error occurred: {}'.format(str(e))}), 500

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'An unexpected error occurred: {}'.format(str(e))}), 500
        
    @app.route('/host-events', methods=['GET'])
    @jwt_required()
    def host_events():
            """
            Get a list of events hosted by the current user.
            Requires user authentication (JWT).
            """
            current_user = get_jwt_identity()
            
            user_id = current_user.get('user_id')	
            events = Event.query.filter_by(host_id=user_id).all()
            events_data = [
                {
                    'event_id': event.event_id,
                    'event_name': event.event_name,
                    'event_description': event.event_description,
                    'event_location': event.event_location,
                    'event_date': event.event_date.strftime('%Y-%m-%dT%H:%M'),
                    'event_status': event.event_status,
                    'event_poster': event.event_poster
                }
                for event in events
            ]
            return jsonify(events_data)

    @app.route('/host/payment-account', methods=['GET', 'POST'])
    @jwt_required()
    def payment_account():
        """
        Get or create a payment account for the current user.
        Requires user authentication (JWT).
        """
        current_user = get_jwt_identity()
        if current_user.get('role') != 'EventHost':
            return jsonify({'error': 'Unauthorized access'}), 403

        if request.method == 'GET':
            try:
                payment_account = PaymentAccount.query.filter_by(host_id=current_user.get('user_id')).first()

                if payment_account:
                    account_data = {
                        'stripe_account_id': payment_account.stripe_account_id,
                        'mpesa_number': payment_account.mpesa_number
                    }
                else:
                    account_data = {}

                return jsonify(account_data), 200

            except Exception as e:
                return jsonify({'error': f'Failed to retrieve payment account details: {str(e)}'}), 500

        elif request.method == 'POST':
            form_data = request.get_json()

            stripe_account_id = form_data.get('stripe_account_id')
            mpesa_number = form_data.get('mpesa_number')

            try:
                payment_account = PaymentAccount.query.filter_by(host_id=current_user.get('user_id')).first()

                if payment_account:
                    payment_account.stripe_account_id = stripe_account_id
                    payment_account.mpesa_number = mpesa_number
                else:
                    payment_account = PaymentAccount(
                        host_id=current_user.get('user_id'),
                        stripe_account_id=stripe_account_id,
                        mpesa_number=mpesa_number
                    )
                    db.session.add(payment_account)

                db.session.commit()
                return jsonify({'message': 'Payment account details saved successfully'}), 200

            except Exception as e:
                db.session.rollback()
                return jsonify({'error': f'Failed to save payment account details: {str(e)}'}), 500
  
    @app.route('/host/reports', methods=['GET'])
    @jwt_required()
    def host_reports():
        """
        Display the host reports page.
        Requires user authentication and event host role.
        """
        try:
            current_user = get_jwt_identity()
            if current_user.get('role') != 'EventHost':	
                return jsonify({'error': 'Unauthorized access'}), 403

            host_events = Event.query.filter_by(host_id=current_user.get('user_id')).all()

            report_data = []

            for event in host_events:
                transactions = db.session.query(Transaction, User).join(User, Transaction.user_id == User.user_id)\
                    .filter(Transaction.event_id == event.event_id).all()

                total_sales = sum(transaction.Transaction.amount_paid for transaction in transactions if transaction.Transaction.payment_status == 'Success')

                total_tickets = event.event_capacity
                tickets_sold = len([transaction.Transaction for transaction in transactions if transaction.Transaction.payment_status == 'Success'])
                tickets_unsold = total_tickets - tickets_sold

                report_data.append({
                    'event_id': event.event_id,
                    'event_name': event.event_name,
                    'event_date': event.event_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'event_location': event.event_location,
                    'event_category': event.event_category,
                    'total_sales': total_sales,
                    'tickets_sold': tickets_sold,
                    'tickets_unsold': tickets_unsold,
                    'transactions': [
                        {
                            'transaction_id': transaction.Transaction.transaction_id,
                            'username': transaction.User.username,
                            'amount_paid': transaction.Transaction.amount_paid,
                            'payment_status': transaction.Transaction.payment_status,
                            'transaction_date': transaction.Transaction.transaction_date.strftime('%Y-%m-%d %H:%M:%S')
                        } for transaction in transactions
                    ]
                })

            return jsonify(report_data), 200

        except Exception as e:
            return jsonify({'error': f'Failed to retrieve reports: {str(e)}'}), 500

    @app.route('/notifications', methods=['GET'])
    @jwt_required()
    def get_notifications():
        try:
            current_user = get_jwt_identity()
            user_id = current_user.get('user_id')

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

        except Exception as e:
            print(f"Error retrieving notifications for user {user_id}: {str(e)}")
            return jsonify({'error': f'Failed to retrieve notifications: {str(e)}'}), 500

    @app.route('/notifications/unread-count', methods=['GET'])
    @jwt_required()
    def get_unread_notification_count():
        try:
            current_user = get_jwt_identity()
            user_id = current_user.get('user_id')
            
            unread_count = Notification.query.filter_by(user_id=user_id, is_read=False).count()
            return jsonify({'unread_count': unread_count})
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve unread count: {str(e)}'}), 500

    @app.route('/notifications/mark-as-read', methods=['POST'])
    @jwt_required()
    def mark_notifications_as_read():
        try:
            current_user = get_jwt_identity()
            user_id = current_user.get('user_id')
            
            Notification.query.filter_by(user_id=user_id, is_read=False).update({'is_read': True})
            db.session.commit()

            return jsonify({'message': 'Notifications marked as read successfully'})
        except Exception as e:
            return jsonify({'error': f'Failed to mark notifications as read: {str(e)}'}), 500
    
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
    def get_attendee_notifications():
        """
        Retrieve notifications for the current attendee.
        """
        try:
            current_user = get_jwt_identity()
            user_id = current_user.get('user_id')

            # Fetch notifications for the user
            notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()

            notifications_data = []
            for notification in notifications:
                # Split and parse event details from the message, if applicable
                if 'is approaching on' in notification.message:
                    try:
                        event_name, event_date_str = notification.message.split(' is approaching on ')
                        event_date = datetime.strptime(event_date_str, '%Y-%m-%d %H:%M')
                    except (ValueError, IndexError):
                        continue  # Skip improperly formatted messages

                    # Mark past event notifications as read
                    if event_date < datetime.utcnow():
                        notification.is_read = True
                        db.session.commit()

                notifications_data.append({
                    'message': notification.message,
                    'is_read': notification.is_read,
                    'created_at': notification.created_at.strftime('%Y-%m-%d %H:%M:%S')
                })

            return jsonify({'notifications': notifications_data}), 200

        except Exception as e:
            print(f"Error retrieving notifications: {e}")
            return jsonify({'error': 'Failed to retrieve notifications'}), 500


    @app.route('/notifications/mark-as-read', methods=['POST'])
    @jwt_required()
    def mark_admin_notifications_as_read():
        """
        Marks all unread notifications for the current user as read.
        """
        current_user = get_jwt_identity()
        
        if current_user.get('role') != 'Admin':	
            return jsonify({'error': 'Unauthorized access'}), 403

        event = Event.query.get('event_id')
        if not event:
            return jsonify({'error': 'Event not found'}), 404

        data = request.json
        status = data.get('status')
        reason = data.get('reason', '')

        if status not in ['Approved', 'Rejected']:
            return jsonify({'error': 'Invalid status provided'}), 400

        event.event_status = status

        action = f'Event_{status.lower()}'
        log = UserInteraction(user_id=current_user.get('user_id'), username=current_user.get('username'), action=action)
        db.session.add(log)

        if status == 'Rejected':
            event.rejection_reason = reason 

        db.session.commit()

        return jsonify({'success': True}), 200

    @app.route('/admin-dashboard')
    @jwt_required()
    def admin_dashboard():
        """
        Display the admin dashboard page.
        Requires user authentication and admin role.
        """
        current_user = get_jwt_identity()
        
        if current_user.get('role') != 'Admin':
            return jsonify({'error': 'Unauthorized access'}), 403

        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/admin/manage-events')
    @jwt_required()
    def manage_events():
        """
        Display the manage events page.
        Requires user authentication and admin role.
        """
        current_user = get_jwt_identity()
        
        if current_user.get('role') != 'Admin':	
            return jsonify({'error': 'Unauthorized access'}), 403
        return send_from_directory(app.static_folder, 'index.html')
     
    @app.route('/api/admin/event-counters', methods=['GET'])
    @jwt_required()
    def get_event_counters():
        """
        Returns the count of events with different statuses (pending, approved, rejected).
        """
        current_user = get_jwt_identity()
        if current_user.get('role') != 'Admin':
            return jsonify({'error': 'Unauthorized access'}), 403

        pending_count = Event.query.filter_by(event_status='Pending').count()
        approved_count = Event.query.filter_by(event_status='Approved').count()
        rejected_count = Event.query.filter_by(event_status='Rejected').count()

        return jsonify({
            'pending': pending_count,
            'approved': approved_count,
            'rejected': rejected_count
        })

    @app.route('/api/admin/profile-counters')
    @jwt_required()
    def get_profile_counters():
        """	
        Get the number of pending, approved, and rejected profiles.
        Requires user authentication and admin role.
        """
        current_user = get_jwt_identity()
        
        if current_user.get('role') != 'Admin':
            return jsonify({'error': 'Unauthorized access'}), 403
        
        pending_count = Profile.query.filter_by(status='Pending').count()
        approved_count = Profile.query.filter_by(status='Approved').count()
        rejected_count = Profile.query.filter_by(status='Rejected').count()
        
        return jsonify({
            'pending': pending_count,
            'approved': approved_count,
            'rejected': rejected_count
        })

    @app.route('/api/admin/profiles', methods=['GET'])
    @jwt_required()
    def get_profiles_by_status():
        """
        Get a list of profiles by status.
        Requires user authentication and admin role.
        """
        current_user = get_jwt_identity()
        
        if current_user.get('role') != 'Admin':
            return jsonify({'error': 'Unauthorized access'}), 403

        status = request.args.get('status')
        if status not in ['Pending', 'Approved', 'Rejected']:
            return jsonify({'error': 'Invalid status'}), 400

        profiles = Profile.query.filter_by(status=status).all()
        profiles_data = [
            {
                'user_id': profile.user_id,
                'username': User.query.filter_by(user_id=profile.user_id).first().username,
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'host_type': profile.host_type,
            }
            for profile in profiles
        ]
        
        return jsonify(profiles_data)

    @app.route('/admin/vetting/<int:user_id>', methods=['GET'])
    @jwt_required()
    def view_vetting_information(user_id):
        """	
        Get the vetting information of a user.
        Requires user authentication and admin role.
        """
        current_user = get_jwt_identity()
        
        if current_user.get('role') != 'Admin':
            return jsonify({'error': 'Unauthorized access'}), 403

        profile = Profile.query.filter_by(user_id=user_id).first()
        if not profile:
            return jsonify({'error': 'Profile not found'}), 404

        profile_data = {
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'phone_number': profile.phone_number,
            'address': profile.address,
            'host_type': profile.host_type,
            'document_id': profile.document_id,
            'business_certificate': profile.business_certificate,
            'status': profile.status
        }
        
        return jsonify(profile_data)

    @app.route('/admin/vetting/update/<int:user_id>', methods=['POST'])
    @jwt_required()
    def update_profile_status(user_id):
        """
        Update the status of a user's profile.
        Requires user authentication and admin role.
        """
        current_user = get_jwt_identity()

        if current_user.get('role') != 'Admin':
            return jsonify({'error': 'Unauthorized access'}), 403

        profile = Profile.query.filter_by(user_id=user_id).first()

        if not profile:
            return jsonify({'error': 'Profile not found'}), 404

        data = request.json
        status = data.get('status')

        if status not in ['Approved', 'Rejected']:
            return jsonify({'error': 'Invalid status provided'}), 400

        profile.status = status

        try:
            log = UserInteraction(
                user_id=current_user['user_id'],  
                username=current_user['username'], 
                action=f'Profile_{status.lower()}'
            )
            db.session.add(log)

            notification_message = "Your profile has been approved." if status == "Approved" else "Your profile has been rejected."
            notification = Notification(
                user_id=user_id,
                message=notification_message,
                is_read=False
            )
            db.session.add(notification)

            db.session.commit()

            return jsonify({'success': True}), 200

        except Exception as e:
            db.session.rollback()

            return jsonify({'error': 'Database commit failed'}), 500

    @app.route('/admin/view-logs', methods=['GET'])
    @jwt_required()
    def view_logs():
        """
        Display the user interactions in the admin logs
        Requires user authentication and admin role.
        """
        try:
            current_user = get_jwt_identity()
            if current_user.get('role') != 'Admin':
                return jsonify({'error': 'Unauthorized access'}), 403

            page = request.args.get('page', 1, type=int)
            action_filter = request.args.get('action', None, type=str)
            username_search = request.args.get('username', None, type=str)

            query = UserInteraction.query

            if action_filter:
                query = query.filter(UserInteraction.action.ilike(f"%{action_filter}%"))


            if username_search:
                query = query.filter(UserInteraction.username.ilike(f"%{username_search}%"))

            pagination = query.order_by(UserInteraction.timestamp.desc()).paginate(page=page, per_page=10, error_out=False)
            interactions = pagination.items

            interactions_data = [
                {
                    'interaction_id': interaction.interaction_id,
                    'user_id': interaction.user_id,
                    'username': interaction.username,
                    'action': interaction.action,
                    'timestamp': interaction.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'event_id': interaction.event_id
                }
                for interaction in interactions
            ]

            return jsonify({
                'interactions': interactions_data,
                'total_pages': pagination.pages,
                'current_page': pagination.page,
                'total_items': pagination.total
            }), 200

        except Exception as e:
            return jsonify({'error': f'Failed to retrieve logs: {str(e)}'}), 500

    @app.route('/api/admin/events', methods=['GET'])
    @jwt_required()
    def get_admin_events():
        """
        Get a list of events.
        Requires user authentication and admin role.
        """
        current_user = get_jwt_identity()
        
        if current_user.get('role') != 'Admin':
            return jsonify({'error': 'Unauthorized access'}), 403
        
        events = Event.query.all()
        events_data = [
            {
                'event_id': event.event_id,
                'event_name': event.event_name,
                'event_description': event.event_description,
                'event_location': event.event_location,
                'event_date': event.event_date.strftime('%Y-%m-%dT%H:%M'),
                'event_status': event.event_status,
                'event_poster': event.event_poster,
                'event_category': event.event_category,
            }
            for event in events
        ]
        
        return jsonify(events_data)

    @app.route('/admin/event/update-status/<int:event_id>', methods=['POST'])
    @jwt_required()
    def update_event_status(event_id):
        """
        Update the status of an event.
        Requires user authentication and admin role.
        """
        current_user = get_jwt_identity()
        
        if current_user.get('role') != 'Admin':	
            return jsonify({'error': 'Unauthorized access'}), 403

        event = Event.query.get(event_id)
        if not event:
            return jsonify({'error': 'Event not found'}), 404

        data = request.json
        status = data.get('status')
        reason = data.get('reason', '')

        if status not in ['Approved', 'Rejected']:
            return jsonify({'error': 'Invalid status provided'}), 400

        event.event_status = status

        action = f'Event_{status.lower()}'
        log = UserInteraction(user_id=current_user.get('user_id'), username=current_user.get('username'), action=action)
        db.session.add(log)

        if status == 'Approved':
            message = f"{event.event_name} has been approved."
        elif status == 'Rejected':
            message = f"{event.event_name} has been rejected - {reason}"

        notification = Notification(
            user_id=event.host_id, 
            message=message,
            is_read=False
        )
        db.session.add(notification)

        if status == 'Rejected':
            event.rejection_reason = reason 

        db.session.commit()

        return jsonify({'success': True}), 200

    @app.route('/api/admin/users', methods=['GET'])
    @jwt_required()
    def get_users():
        """
        Get a list of users.
        Requires user authentication and admin role.
        """
        current_user = get_jwt_identity()
        
        if current_user.get('role') != 'Admin':	
            return jsonify({'error': 'Unauthorized access'}), 403

        users = User.query.all()
        users_data = [
            {
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'status': user.status,
            }
            for user in users
        ]
        
        return jsonify(users_data)

    @app.route('/api/admin/user-status/<int:user_id>', methods=['POST'])
    @jwt_required()
    def toggle_user_status(user_id):
        """
        Change the status of a user.
        Requires user authentication and admin role.
        """
        current_user = get_jwt_identity()
        
        if current_user.get('role') != 'Admin':
            return jsonify({'error': 'Unauthorized access'}), 403

        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        if user.status == 'active':
            user.status = 'blocked'
           
            log = UserInteraction(user_id=current_user.get('user_id'), username=current_user.get('username'), action='User_blocked')
            db.session.add(log)
            db.session.commit()
        else:
            user.status = 'active'
            
            log = UserInteraction(user_id=current_user.get('user_id'), username=current_user.get('username'), action='User_unblocked')
            db.session.add(log)
            db.session.commit()

        db.session.commit()
        return jsonify({'success': True}), 200

    @app.route('/admin/create-admin', methods=['POST'])
    @jwt_required()
    def create_admin():
        """	
        Create an admin user.
        Requires user authentication and admin role.
        """
        try:
            current_user = get_jwt_identity()
            if current_user.get('role') != 'Admin':
                return jsonify({'error': 'Unauthorized access'}), 403

            data = request.json
            if not data:
                return jsonify({'error': 'No data provided in request'}), 400

            required_fields = ['name', 'surname', 'phone_number', 'email', 'country', 'password', 'username']
            missing_fields = [field for field in required_fields if field not in data]

            if missing_fields:
                return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

            existing_user = User.query.filter((User.username == data['username']) | (User.email == data['email'])).first()
            if existing_user:
                return jsonify({'error': 'Username or email already exists'}), 400

            new_admin = User(
                username=data['username'],
                email=data['email'],
                role='Admin',
                status='active',
                created_at=datetime.utcnow()
            )
            new_admin.set_password(data['password']) 
            db.session.add(new_admin)
            db.session.flush() 

            admin_details = AdminDetails(
                admin_id=new_admin.user_id, 
                name=data['name'],
                surname=data['surname'],
                phone_number=data['phone_number'],
                country=data['country']
            )

            db.session.add(admin_details)
            db.session.commit()

            return jsonify({'message': 'Admin created successfully'}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to create admin: {str(e)}'}), 500

    @app.route('/change-password', methods=['POST'])
    @jwt_required()
    def change_password():
        """	
        Change the password of the current user.
        Requires user authentication (JWT). 
        """
        try:
            current_user = get_jwt_identity()
            
            data = request.json
            old_password = data.get('old_password')
            new_password = data.get('new_password')

            if not current_user.check_password(old_password):
                return jsonify({'error': 'Old password is incorrect'}), 400

            current_user.set_password(new_password)
            db.session.commit()

            return jsonify({'message': 'Password changed successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to change password'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
