from flask import jsonify
from hello_books import app


@app.errorhandler(404)
def not_found(error):
    return jsonify(dict(error='Resource not found')), 404

