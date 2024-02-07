# services for the applications once we hit a route

from flask import make_response, jsonify
from util import is_database_connected
from main import User

def create_user_record(database, user):
    
    database.session.add(user)
    database.session.commit()
    database.session.refresh(user)
    user_details = user.get_user()
    return jsonify(user_details), 201


def update_user_record(database, user, fields_to_update, bcrypt):
    
    user.first_name = fields_to_update.get('first_name',user.first_name)
    user.last_name  = fields_to_update.get('last_name',user.last_name)
    
    if fields_to_update.get('password'):
        hashedPassword = bcrypt.generate_password_hash(fields_to_update['password']).decode('utf-8')
        user.password  = hashedPassword
    
    database.session.commit()

    return make_response('',204)


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