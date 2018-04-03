from flask import jsonify
from hello_books import app


@app.errorhandler(404)
def not_found(error):
    return jsonify(dict(error='Resource not found')), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(dict(error='Method not allowed')), 405


@app.errorhandler(500)
def server_error(error):
    return jsonify(dict(error='Internal server error')), 500


@app.errorhandler(400)
def bad_request(error):
    return jsonify(dict(error='Bad Request')), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify(dict(error='Unauthorized to access this information')), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify(dict(error='Forbidden')), 403


@app.errorhandler(409)
def conflict(error):
    return jsonify(dict(error='Conflict')), 409
