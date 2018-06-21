from api import create_app
import os

config_name = 'development'
app = create_app(config_name)

if __name__ == '__main__':
    PORT = int(os.getenv('PORT', 5000))
    app.run('127.0.0.0=1',port=PORT)
