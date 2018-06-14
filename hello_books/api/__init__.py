'''Import Dependances'''
from flask import jsonify
from hello_books import create_app

app = create_app('development')


@app.errorhandler(404)
def not_found(error):
    '''Error message for 404 not found'''
    return jsonify(dict(error='Resource not found')), 404


@app.errorhandler(405)
def method_not_allowed(error):
    '''Error message for 405 method not allowed'''
    return jsonify(dict(error='Method not allowed')), 405


@app.errorhandler(500)
def server_error(error):
    '''Error message for 500 server error'''
    return jsonify(dict(error='Internal server error')), 500


@app.errorhandler(400)
def bad_request(error):
    '''Error message for 400 bad request'''
    return jsonify(dict(error='Bad Request')), 400


@app.errorhandler(401)
def unauthorized(error):
    '''Error message for 401 unauthorized access'''
    return jsonify(dict(error='Unauthorized to access this information')), 401


@app.errorhandler(403)
def forbidden(error):
    '''Error message for 403, forbidden'''
    return jsonify(dict(error='Forbidden')), 403


@app.errorhandler(409)
def conflict(error):
    '''Érror message for 409, conflict'''
    return jsonify(dict(error='Conflict')), 409


