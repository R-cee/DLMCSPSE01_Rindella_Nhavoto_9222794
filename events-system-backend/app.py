import os, pymysql
from models import db, User, UserInteraction, Profile
from flask import Flask, jsonify, request, redirect, url_for, send_from_directory
from flask_login import LoginManager, logout_user
from datetime import timedelta
from flask_cors import CORS
from config import Config
from flask import request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

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

            access_token = create_access_token(identity={'user_id': user.user_id, 'role': user.role})
            
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

    @app.route('/uploads/certs/<filename>')
    def uploaded_cert_file(filename):
        """
        Display the business certificate image.
        """
        return send_from_directory(app.config['UPLOAD_CERT'], filename)
      
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


if __name__ == '__main__':
    app.run(debug=True)
