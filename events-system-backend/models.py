from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import create_engine
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """
    User profile model for storing user information.
    Attributes:
    - user_id: Primary key.
    - username: Unique username.
    - email: Unique email address.
    - password: Hashed password.
    - role: Role of the user ('Admin', 'EventHost', 'Attendee').
    - status: Status of the user ('active' or 'blocked').
    """
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'Admin', 'EventHost', 'Attendee'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default="active")  # 'active' or 'blocked'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.user_id)

class Event(db.Model):
    """
    Event model representing events created by Event Hosts.
    Attributes:
        event_id: Primary key, unique identifier for each event.
        host_id: Foreign key linking to the user who created the event.
        event_name: Name of the event.
        event_description: Description of the event.
        event_category: Category of the event.
        event_country: Country where the event will be held.
        event_location: Location where the event will be held.
        event_date: Date and time of the event.
        event_price: Price of the event ticket.
        event_capacity: Maximum number of attendees allowed for the event.
        event_poster: Path to the event poster image.
        event_status: Status of the event, can be 'Pending', 'Approved', or 'Rejected'.
        created_at: Timestamp when the event was created.
    """
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    event_name = db.Column(db.String(100), nullable=False)
    event_description = db.Column(db.Text)
    event_category = db.Column(db.String(100), nullable=False) # 'Music', 'Sports', 'Education', 'Culture', 'Arts', 'Food', 'Travel', 'Other'
    event_country = db.Column(db.String(100), nullable=False)
    event_location = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    event_price = db.Column(db.Float, nullable=False)
    event_capacity = db.Column(db.Integer)
    event_poster = db.Column(db.String(200)) 
    event_status = db.Column(db.String(20), default='Pending')  # 'Pending', 'Approved', 'Rejected'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Profile(db.Model):
    """
    Profile model storing additional information about hosts.
    Attributes:
        profile_id: Primary key, unique identifier for each profile.
        user_id: Foreign key linking to the user.
        first_name: First name of the user.
        last_name: Last name of the user.
        phone_number: Phone number of the user.
        address: Address of the user.
        document_id: Path to the identification document uploaded by the user.
        host_type: Type of host ('Individual', 'Business', 'Organization').
        business_certificate: Business certificate if the host is a business or organization.
        status: Status of the profile, can be 'Pending', 'Approved', 'Rejected'.
    """
    __tablename__ = 'profiles'
    profile_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(200))
    host_type = db.Column(db.String(20), nullable=False)  # 'Individual', 'Business', or 'Organization'
    document_id = db.Column(db.String(200))  # Government ID document
    business_certificate = db.Column(db.String(200))  # Business certificate if the host is a business or organization
    status = db.Column(db.String(20), default='Pending')  # 'Pending', 'Approved', 'Rejected'

class Notification(db.Model):
    """
    Notification model storing messages sent to users.
    Attributes:
        notification_id: Primary key, unique identifier for each notification.
        user_id: Foreign key linking to the user who received the notification.
        message: Content of the notification message.
        is_read: Status indicating whether the notification has been read.
        created_at: Timestamp when the notification was created.
    """
    __tablename__ = 'notifications'
    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Transaction(db.Model):
    """
    Transaction model recording ticket purchases and payment transactions.
    Attributes:
        transaction_id: Primary key, unique identifier for each transaction.
        event_id: Foreign key linking to the event for which the ticket was purchased.
        user_id: Foreign key linking to the user who made the purchase.
        transaction_date: Timestamp when the transaction occurred.
        payment_status: Status of the payment, can be 'Success', 'Failed', or 'Pending'.
        amount_paid: Amount paid for the ticket.
        quantity: Quantity of tickets purchased.
    """
    __tablename__ = 'transactions'
    transaction_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_status = db.Column(db.String(20), nullable=False)  # 'Success', 'Failed', 'Pending'
    amount_paid = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer,  nullable=False)

class UserInteraction(db.Model):
    """
    Model to log user interactions such as login, event creation, payment, likes, and vetting form submission.

    Attributes:
        interaction_id (int): Primary key, unique identifier for each interaction.
        user_id (int): Foreign key linking to the user who performed the action.
        username (str): The username of the user.
        action (str): The action performed by the user (e.g., 'Login', 'Event_created', 'Paid', 'Liked', 'Vetting_form').
        timestamp (datetime): The timestamp when the action was performed.
        event_id (int): Foreign key linking to the event that was liked.
    """
    __tablename__ = 'user_interactions'
    interaction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=True)

    def __init__(self, user_id, username, action, event_id=None):
        self.user_id = user_id
        self.username = username
        self.action = action
        self.event_id = event_id

class PaymentAccount(db.Model):
    """
    Model to store payment account details for hosts.
    Attributes:
        payment_account_id (int): Primary key, unique identifier for each payment account.
        host_id (int): Foreign key linking to the host.
        stripe_account_id (str): Stripe account ID.
        mpesa_number (str): M-Pesa number.
    """
    __tablename__ = 'payment_accounts'
    payment_account_id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    stripe_account_id = db.Column(db.String(50))    
    mpesa_number = db.Column(db.String(50))
    
    def __init__(self, host_id, stripe_account_id, mpesa_number):
        self.host_id = host_id
        self.stripe_account_id = stripe_account_id
        self.mpesa_number = mpesa_number
      
# class IntegrationSettings(db.Model):
#     """
#     Model to store integration settings for the application.
#     Attributes:
#         integration_id (int): Primary key, unique identifier for each integration.
#         provider (str): The provider of the integration (e.g., 'Stripe' or 'M-Pesa').
#         api_key (str): The API key for the integration.
#         status (str): The status of the integration (e.g., 'Active' or 'Inactive').
#     """
#     __tablename__ = 'integration_settings'
#     integration_id = db.Column(db.Integer, primary_key=True)
#     provider = db.Column(db.String(50), nullable=False)  # Stripe or M-Pesa
#     api_key = db.Column(db.String(255), nullable=False)
#     status = db.Column(db.String(50), default='Active')  # Active or Inactive  
    
#     def __init__(self, provider, api_key, status):
#         self.provider = provider
#         self.api_key = api_key
#         self.status = status    
      
class AdminDetails(db.Model):
    """
    AdminDetails model to store additional information for admins.
    Attributes:
    - admin_id: Foreign key to User model.
    - name: Admin's name.
    - surname: Admin's surname.
    - phone_number: Admin's phone number.
    - country: Country that the admin manages.
    """
    __tablename__ = 'admin_details'
    admin_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), nullable=False)

    admin = db.relationship('User', backref=db.backref('admin_details', uselist=False))
        
# Location where the database will be created
DATABASE_URL = 'mysql+pymysql://root:P%40ssw0rd24@localhost/events-system'
engine = create_engine(DATABASE_URL)
