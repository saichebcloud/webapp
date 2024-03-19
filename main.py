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

log_module.log(log_level='INFO',log_message='Server Starting up')

class User(database.Model):

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


@app.route('/v1/user', methods=[HTTP_METHODS[1]])
def create_new_user():

    if util.check_request_sent_with_payload(request,auth=True,params=True):
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
            return services.create_user_record(database=database, user=new_user)

    return make_response('',400)


@app.route('/v1/user', methods=HTTP_METHODS[2:].append(HTTP_METHODS[0]))
def unauthorised_create_user_request():
    
    return services.handle_unauthorised_methods()


@app.route('/v1/user/self', methods=[HTTP_METHODS[0],HTTP_METHODS[2]], provide_automatic_options=False)
def get_or_update_user_data():

    if request.method == HTTP_METHODS[2] and util.check_request_sent_with_payload(request, params=True):
        return make_response('',400)
    
    if request.method == HTTP_METHODS[0] and util.check_request_sent_with_payload(request, params=True, body=True):
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
        
        if user and request.method == HTTP_METHODS[0]:
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
    
    if util.check_for_head_method_mapping(request):
        return services.handle_unauthorised_methods()

    if util.check_request_sent_with_payload(request, body=True, params=True, auth=True):
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
    
    user = User.query.filter_by(username=username).first()
    
    if user:
        if user.check_password(password):
            return user
        else:
            return False
    
    else:
        return False


if __name__ == '__main__':
    
    with app.app_context():
        database.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)