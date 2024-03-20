# services for the applications once we hit a route

from flask import make_response, jsonify
from util import is_database_connected
import log_module

def create_user_record(database, user):
    
    database.session.add(user)
    database.session.commit()
    database.session.refresh(user)
    user_details = user.get_user()
    log_module.log(log_level='INFO', log_message=f'User {user_details.username} created succesfully')
    return jsonify(user_details), 201


def update_user_record(database, user, fields_to_update, bcrypt):
    
    user.first_name = fields_to_update.get('first_name',user.first_name)
    user.last_name  = fields_to_update.get('last_name',user.last_name)
    
    if fields_to_update.get('password'):
        hashedPassword = bcrypt.generate_password_hash(fields_to_update['password']).decode('utf-8')
        user.password  = hashedPassword
    
    database.session.commit()
    log_module.log(log_level='INFO', log_message=f'User {user.username} created succesfully')
    return make_response('',204)


def check_database_health(database):
    
    if is_database_connected(database):
        response = make_response('',200)
        log_module.log(log_level='INFO', log_message='Database Connnection OK')
    else:
        response = make_response('',503)
        log_module.log(log_level='ERROR', log_message='Could not connect to database')

    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


def handle_unauthorised_methods():
    log_module.log(log_level='WARNING',log_message='Unauthorised request method')
    return make_response('',405)


def handle_page_not_found():
    log_module.log(log_level='WARNING',log_message='Request endpoint not found')
    return make_response('',404)