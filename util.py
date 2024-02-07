# Utility functions for the application

from sqlalchemy.exc import OperationalError
import re
import base64

def is_database_connected(database):
    
    try:
        with database.engine.connect():
            return True
    
    except OperationalError:
        return False
    
    finally:
        database.engine.dispose()


def check_request_sent_with_payload(request, body=False, params=False, auth=False):

    if params is True and request.args:
        return True
    
    if body is True and (request.form or request.data):
        return True
    
    if auth is True and request.headers.get('Authorization'):
        return True
    
    return False


def check_for_head_method_mapping(request):
    
    return request.method == 'HEAD'


def check_for_options_method_mapping(request):
    
    return request.method == 'OPTIONS'


def validate_email(email):
    
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    return re.match(pattern, email) is not None


def validate_name(name):
    
    pattern = r'^[a-zA-Z]+\s*[a-zA-Z]*\s*$'

    return re.match(pattern,name) is not None


def parse_and_validate_create_user_request(request):

    try:
        requestBody = request.json
    
    except Exception:
        return False
    
    allowed_fields = {'first_name', 'last_name', 'password', 'username'}

    for field in requestBody.keys():
        
        if field not in allowed_fields:
            return False

    user_first_name = requestBody.get('first_name')
    user_last_name  = requestBody.get('last_name')
    user_password   = requestBody.get('password')
    user_username   = requestBody.get('username')

    if not user_first_name or not validate_name(user_first_name) or not user_last_name or not validate_name(user_last_name) or not user_password or not user_username or not validate_email(user_username):
        return False
    
    else:
        return {
            'user_first_name': re.sub(r'\s+',' ',user_first_name).strip(),
            'user_last_name' : re.sub(r'\s+',' ',user_last_name).strip(),
            'user_password'  : user_password,
            'user_username'  : user_username
        }


def parse_and_validate_update_user_request(request):

    try:
        requestBody = request.json
    
    except Exception:
        return False
    
    allowed_updation_fields = {'first_name', 'last_name', 'password'}

    fields_to_update = {}
    
    for field in requestBody.keys():
        
        if field not in allowed_updation_fields:
            return False
        
        else: 
            fields_to_update[field] = requestBody.get(field)
    
    return fields_to_update


def parse_user_credentials(request):
    
    auth_header = request.headers.get('Authorization')
    
    if auth_header and auth_header.startswith('Basic '):
        
        encoded_credentials = auth_header[len('Basic '):]
        credentials         = base64.b64decode(encoded_credentials).decode('utf-8')
        username, password  = credentials.split(':')
        
        if username == '' or password == '':
            return []
        
        return [username,password]
    
    else:
        return []