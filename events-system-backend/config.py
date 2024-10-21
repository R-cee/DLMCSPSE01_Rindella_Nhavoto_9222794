class Config:
    """
    Configuration class for the application.
    Contains settings for secret key, database URI, SQL settings, file upload configurations, and allowed file extensions.
    """
    SECRET_KEY = 'Rinr123'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:P%40ssw0rd24@localhost/events-system'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_EVENT = 'C:/Users/Rindella Nhavoto/Desktop/ProjectsVSC/SWEproject/events-system-backend/event_images'
    UPLOAD_ID = 'C:/Users/Rindella Nhavoto/Desktop/ProjectsVSC/SWEproject/events-system-backend/profile_gov_id'
    UPLOAD_CERT = 'C:/Users/Rindella Nhavoto/Desktop/ProjectsVSC/SWEproject/events-system-backend/profile_cert'
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
