import os
from api import create_app

config_name = 'development'
app = create_app(config_name)

if __name__ == '__main__':
    PORT = os.getenv('PORT', 5000)
    app.run('0.0.0.0',port=PORT)
