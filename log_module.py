import json
import datetime

WEBAPP_LOG_FILE = '/var/log/webapp.log'

def write_to_log(jsonObject):
    
    with open(WEBAPP_LOG_FILE,'a') as log_file:

        json.dump(jsonObject,log_file)
        log_file.write('\n') 


def log(log_level, log_message):

    log_entry = {
        "timeStamp": str(datetime.datetime.now()),
        "severity" : log_level,
        "message" : log_message
    }

    write_to_log(log_entry)