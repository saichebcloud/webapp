# services for the applications once we hit a route

from flask import make_response, jsonify
from util import is_database_connected
import log_module
from google.cloud import pubsub_v1
import json
import secrets
import string

project_id = "devp-414719"
topic_id   = "verify_user"
publisher  = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)


def generate_unique_token(length=16):
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for _ in range(length))
    return token

def create_user_record(database, user, token):
    
    database.session.add(user)
    database.session.commit()
    database.session.refresh(user)
    user_details = user.get_user()
    token_details = token.get_token_info()
    log_module.log(log_level='INFO', log_message=f'User {user_details["username"]} created succesfully')

    data = {
        "email": user_details.get('username'),
        "token": token_details.get('token')
    }

    json_data = json.dumps(data)

    database.session.add(token)
    database.session.commit()
    publisher.publish(topic_path,json_data.encode("utf-8"))

    return jsonify(user_details), 201


def update_user_record(database, user, fields_to_update, bcrypt):
    
    user.first_name = fields_to_update.get('first_name',user.first_name)
    user.last_name  = fields_to_update.get('last_name',user.last_name)
    
    if fields_to_update.get('password'):
        hashedPassword = bcrypt.generate_password_hash(fields_to_update['password']).decode('utf-8')
        user.password  = hashedPassword
    
    database.session.commit()

    log_module.log(log_level='INFO', log_message=f'User {user.username} updated succesfully')

    return make_response('',204)


def check_database_health(database):
    
    if is_database_connected(database):
        response = make_response('',200)
    
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