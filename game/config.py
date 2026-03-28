import os
from dotenv import load_dotenv

load_dotenv()

# using as development config
class Config: 
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///game.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENWEATHER_API_KEY = 'test_openweather_api_key'


# Development Config
# Production Config