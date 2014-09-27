import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/pat2"
    BUILD_DIR = os.path.join(os.getcwd(),'build')
    UPLOAD_DIR = os.path.join(os.getcwd(), 'upload')
    PHOTO_STORE = os.path.join(os.getcwd(),'media/photos')
    RAW_STORE = os.path.join(os.getcwd(),'media/raw')
    CROP_STORE = os.path.join(os.getcwd(),'media/crops')
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    SITE_BUCKET = "www.photosandtext.com"
    DEBUG = False


class DevConfig(Config):
    SITE_BUCKET = "beta.photosandtext.com"
    DEBUG = True