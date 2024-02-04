# Utility functions for the application

from sqlalchemy.exc import OperationalError

def is_database_connected(database):
    try:
        with database.engine.connect():
            return True
    except OperationalError:
        return False
    finally:
        database.engine.dispose()

def check_request_sent_with_payload(request):
    if request.args or request.form or request.data:
        return True
    else:
        return False

def check_for_head_method_mapping(request):
    return request.method == 'HEAD'