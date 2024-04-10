from flask import Flask,request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from pymysql import OperationalError
from config import configure_database
from flask_bcrypt import Bcrypt
from datetime import datetime
import uuid
import services
import util
import log_module

HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'TRACE', 'PATCH', 'HEAD', 'OPTIONS']

app = Flask(__name__)
configure_database(app)
database = SQLAlchemy(app)

bcrypt = Bcrypt()

log_module.log(log_level='DEBUG',log_message='Server Starting up')

class Token(database.Model):

    token     = database.Column(database.String(20),primary_key=True)
    email     = database.Column(database.String(50))
    timestamp = database.Column(database.DateTime, default=datetime.utcnow)
    status    = database.Column(database.String(15))

    def __init__(self,token,status,email):
        self.email = email
        self.token = token
        self.status = status
    
    def get_token_info(self):
        return {
            'token': self.token,
            'email': self.email,
            'timestamp': self.timestamp,
            'status': self.status
        }


class User(database.Model):

    log_module.log(log_level='INFO',log_message='Received request to create user')

    id              = database.Column(database.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    first_name      = database.Column(database.String(50))
    last_name       = database.Column(database.String(50))
    username        = database.Column(database.String(120), unique=True)
    password        = database.Column(database.String(80))
    account_created = database.Column(database.DateTime, default=datetime.utcnow)
    account_updated = database.Column(database.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, first_name, last_name, username, password):
        self.first_name = first_name
        self.last_name  = last_name
        self.username   = username
        self.password   = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def get_user(self):
        return {
            'id': str(self.id),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'account_created': self.account_created,
            'account_updated': self.account_updated
        }
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

@app.route('/verify',methods=[HTTP_METHODS[0]])
def verify_user():

    if util.check_request_sent_with_payload(request,auth=True,body=True):
        log_module.log(log_level='WARNING',log_message='Request sent with unexpected payload')
        return make_response('',400)

    token = request.args.get('token')

    token_record = Token.query.filter_by(token=token).first()

    if not token_record:
        return make_response('Invalid Token',400)

    token_details = token_record.get_token_info()
    time = str(token_details.get('timestamp'))
    timestamp_format = "%Y-%m-%d %H:%M:%S"


    timestamp = datetime.strptime(time, timestamp_format)
    current_time = datetime.utcnow()

# Calculate time difference
    time_difference = current_time - timestamp

# Convert time difference to minutes
    minutes_difference = time_difference.total_seconds() / 60


    if minutes_difference < 2:
        token_record.status = 'VERIFIED'
        database.session.commit()
        return make_response('verfied',200)

    return make_response('Link expired',410)


@app.route('/verify', methods=HTTP_METHODS[1:])
def unauthorised_verify_user():

    return services.handle_unauthorised_methods()


@app.route('/v1/user', methods=[HTTP_METHODS[1]])
def create_new_user():

    if util.check_request_sent_with_payload(request,auth=True,params=True):
        log_module.log(log_level='WARNING',log_message='Request sent with unexpected payload')
        return make_response('',400)

    if request.is_json:

        user_details = util.parse_and_validate_create_user_request(request)
        
        if user_details:

            database.engine.dispose()

            db_response = services.check_database_health(database)

            if db_response.status_code != 200:
                return db_response

        if user_details and User.query.filter_by(username=user_details['user_username']).first() is None:

            new_user = User(first_name=user_details['user_first_name'], last_name=user_details['user_last_name'], username=user_details['user_username'] , password=user_details['user_password'] )
            token = services.generate_unique_token()
            new_token = Token(email=user_details['user_username'],token=token,status="PENDING")
            print(new_token.get_token_info())
            return services.create_user_record(database=database, user=new_user, token=new_token)
        
        log_module.log(log_level='WARNING',log_message='Attempt to create user with existing username')
    
    log_module.log(log_level='WARNING',log_message='Request payload is incorrect')

    return make_response('',400)


@app.route('/v1/user', methods=HTTP_METHODS[2:].append(HTTP_METHODS[0]))
def unauthorised_create_user_request():
    
    return services.handle_unauthorised_methods()


@app.route('/v1/user/self', methods=[HTTP_METHODS[0],HTTP_METHODS[2]], provide_automatic_options=False)
def get_or_update_user_data():

    log_module.log(log_level='INFO',log_message='Received request to get/update user')

    if request.method == HTTP_METHODS[2] and util.check_request_sent_with_payload(request, params=True):
        log_module.log(log_level='WARNING',log_message='Request sent with unexpected payload')
        return make_response('',400)
    
    if request.method == HTTP_METHODS[0] and util.check_request_sent_with_payload(request, params=True, body=True):
        log_module.log(log_level='WARNING',log_message='Request sent with unexpected payload')
        return make_response('', 400)

    if util.check_for_head_method_mapping(request):
        return services.handle_unauthorised_methods()

    user_credentials = util.parse_user_credentials(request)

    if user_credentials:

        database.engine.dispose()

        db_response = services.check_database_health(database)

        if db_response.status_code != 200:
            return db_response

        user = is_user_authenticated(user_credentials)

        token = Token.query.filter_by(email=user_credentials[0],status='VERIFIED').first()

        if user and not token:
            return make_response('',403)
        
        if user and request.method == HTTP_METHODS[0]:
            log_module.log(log_level='INFO',log_message='GET user request received, returning user details')
            return jsonify(user.get_user()), 200
        
        elif user and request.method == HTTP_METHODS[2]:
            fields_to_update = util.parse_and_validate_update_user_request(request)

            if fields_to_update:
                return services.update_user_record(database=database, user=user, fields_to_update=fields_to_update, bcrypt=bcrypt)
            
            else:
                return make_response('',400)
            
        else:
            return make_response('',401)
    else:
        return make_response('',400)


@app.route('/v1/user/self', methods=HTTP_METHODS[1:])
def unauthorised_get_user_request():
    
    return services.handle_unauthorised_methods()


@app.route('/healthz', methods=[HTTP_METHODS[0]], provide_automatic_options=False)
def health_check():

    log_module.log(log_level='INFO',log_message='Received request for database health')
    
    if util.check_for_head_method_mapping(request):
        return services.handle_unauthorised_methods()

    if util.check_request_sent_with_payload(request, body=True, params=True, auth=True):
        log_module.log(log_level='WARNING',log_message='Request sent with unexpected payload')
        return make_response('',400)

    return services.check_database_health(database)


@app.route('/healthz', methods=HTTP_METHODS[1:])
def unauthorised_health_request():
    
    return services.handle_unauthorised_methods()


@app.errorhandler(404)
def page_not_found(error):
    
    return services.handle_page_not_found()


def is_user_authenticated(credentials):
    
    username,password = credentials
    
    user  = User.query.filter_by(username=username).first()
    
    if user:
        if user.check_password(password):
            return user
        else:
            log_module.log(log_level='WARNING',log_message='Could not authenticate user')
            return False
    
    else:
        log_module.log(log_level='ERROR',log_message='Could not recognize username or username not verified')
        return False


if __name__ == '__main__':
    
    with app.app_context():
        database.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)