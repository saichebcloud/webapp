# This file will have the configurations required for the application

from dotenv import load_dotenv
import pymysql
import os

load_dotenv()
pymysql.install_as_MySQLdb()

def configure_database(app):
    db_user     = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host     = os.getenv("DB_HOST")
    db_port     = os.getenv("DB_PORT")
    db_name     = os.getenv("DB_NAME")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'