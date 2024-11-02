import os

class Config:
    """
    Configuration class for the application.
    Contains settings for secret key, database URI, SQL settings, file upload configurations, and allowed file extensions.
    """
    SECRET_KEY = 'Rinr123'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:P%40ssw0rd24@localhost/events-system-db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_EVENT = 'C:/Users/Rindella Nhavoto/Desktop/ProjectsVSC/SWEproject/EventsGit/DLMCSPSE01_Rindella_Nhavoto_9222794/events-system-backend/event_images'
    UPLOAD_ID = 'C:/Users/Rindella Nhavoto/Desktop/ProjectsVSC/SWEproject/EventsGit/DLMCSPSE01_Rindella_Nhavoto_9222794/events-system-backend/profile_gov_id'
    UPLOAD_CERT = 'C:/Users/Rindella Nhavoto/Desktop/ProjectsVSC/SWEproject/EventsGit/DLMCSPSE01_Rindella_Nhavoto_9222794/events-system-backend/profile_cert'
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
    STRIPE_SECRET_KEY = 'sk_test_51Q9xXHP5Lv2xb3IZKkyE6Dhh9WuVKx30sTt9b83BlgXL4THFKbbWCVIRJ1JaeHxk0J46oEArSxZGnYK45HbG69yw0072XMGkWh'