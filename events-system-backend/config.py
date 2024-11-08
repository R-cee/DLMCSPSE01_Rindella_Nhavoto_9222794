import os

class Config:
    """
    Configuration class for the application.
    Contains settings for secret key, database URI, SQL settings, file upload configurations, and allowed file extensions.
    """
    SECRET_KEY = 'Rinr123'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:P%40ssw0rd24@localhost:3306/events-system-db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #Paths in remote Amazon EC2 instance
    UPLOAD_EVENT = '/home/ec2-user/events_app/events-system-backend/event_images'
    UPLOAD_ID = '/home/ec2-user/events_app/events-system-backend/profile_cert'
    UPLOAD_CERT = '/home/ec2-user/events_app/events-system-backend/profile_gov_id'
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
    STRIPE_SECRET_KEY = 'sk_test_51Q9xXHP5Lv2xb3IZKkyE6Dhh9WuVKx30sTt9b83BlgXL4THFKbbWCVIRJ1JaeHxk0J46oEArSxZGnYK45HbG69yw0072XMGkWh'