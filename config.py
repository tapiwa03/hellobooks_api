class Config:
    """Parent config class"""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = 'Some-Key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgre:test1234@localhost:5432/hellobooks'

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


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
