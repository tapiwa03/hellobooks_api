import datetime
'''
class Config:
    """Parent config class"""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = 'Some-Key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgre:test1234@localhost:5432/hellobooks'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """Configurations for development"""
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgre:test1234@localhost:5432/test_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
'''
class BaseConfig:
    """Base configuration"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'Random-Key_1to3'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=45)


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:test1234@localhost/hellobooks"



class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:test1234@localhost/testdb"
    PRESERVE_CONTEXT_ON_EXCEPTION = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
