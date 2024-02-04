from flask import Flask,request, make_response
from flask_sqlalchemy import SQLAlchemy
from config import configure_database
import services
import util

HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'TRACE', 'PATCH', 'HEAD', 'OPTIONS']

app = Flask(__name__)
configure_database(app)
database = SQLAlchemy(app)

@app.route('/healthz', methods=[HTTP_METHODS[0]], provide_automatic_options=False)
def health_check():
    if util.check_for_head_method_mapping(request):
        return services.handle_unauthorised_methods()

    if util.check_request_sent_with_payload(request) is True:
        return make_response('',400)

    return services.check_database_health(database)

@app.route('/healthz', methods=HTTP_METHODS[1:])
def unauthorised_health_request():
    return services.handle_unauthorised_methods()

@app.errorhandler(404)
def page_not_found(error):
    return services.handle_page_not_found()



if __name__ == '__main__':
    with app.app_context():
        database.create_all()
    app.run()