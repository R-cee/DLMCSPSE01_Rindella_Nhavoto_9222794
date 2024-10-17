import os, pymysql
from models import db, User, UserInteraction, Notification, Profile, Event, Transaction, PaymentAccount
from flask import Flask, jsonify, request, redirect, url_for, send_from_directory
from flask_login import LoginManager, logout_user, current_user
from datetime import timedelta, datetime
from flask_cors import CORS
from config import Config
from flask import request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError

app = Flask(__name__, static_folder='../events-system-frontend/build', static_url_path='')
CORS(app)

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
            
            access_token = create_access_token(identity={'user_id': user.user_id, 'role': user.role, 'username': user.username})


            if user.role == 'Attendee':
                redirect_url = '/landing'
            elif user.role == 'EventHost':
                redirect_url = '/host-dashboard'
            elif user.role == 'Admin':
                redirect_url = '/admin-dashboard'
            else:
                return jsonify({'errors': 'Invalid user role'}), 400

            return jsonify({'access_token': access_token, 'redirect': redirect_url, 'username': user.username, 'role': user.role}), 200
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

    @app.route('/host-dashboard')
    def host_dashboard():
        """
        Display the host dashboard page.
        """
        return send_from_directory(app.static_folder, 'index.html')
    
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
    
    @app.route('/vetting', methods=['POST'])
    @jwt_required()
    def vetting():
        """
        Submit vetting form data.
        Requires user authentication (JWT).
        """
        current_user = get_jwt_identity()
        
        user_id = current_user.get('user_id')
        
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
                transactions = Transaction.query.filter_by(event_id=event.event_id).all()
                total_sales = sum(transaction.amount_paid for transaction in transactions if transaction.payment_status == 'Success')

                total_tickets = event.event_capacity
                tickets_sold = len([transaction for transaction in transactions if transaction.payment_status == 'Success'])
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
                            'transaction_id': transaction.transaction_id,
                            'user_id': transaction.user_id,
                            'amount_paid': transaction.amount_paid,
                            'payment_status': transaction.payment_status,
                            'transaction_date': transaction.transaction_date.strftime('%Y-%m-%d %H:%M:%S')
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

            if notifications:
                notifications_data = [
                    {
                        'message': notification.message,
                        'is_read': notification.is_read,
                        'created_at': notification.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    for notification in notifications
                ]
                return jsonify({'notifications': notifications_data}), 200
            else:
                return jsonify({'notifications': []}), 200

        except Exception as e:
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
    
if __name__ == '__main__':
    app.run(debug=True)
