import datetime
class BaseConfig:
    """Base configuration"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'Random-Key_1to3'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=45)


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:@localhost/hellobooks"



class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:@localhost/testdb"
    PRESERVE_CONTEXT_ON_EXCEPTION = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
