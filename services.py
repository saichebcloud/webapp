# services for the applications once we hit a route

from flask import make_response
from util import is_database_connected

def check_database_health(database):
    if is_database_connected(database):
        response = make_response('',200)
    else:
        response = make_response('',503)
    
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

def handle_unauthorised_methods():
    return make_response('',405)

def handle_page_not_found():
    return make_response('',404)