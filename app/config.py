import os
from dotenv import load_dotenv
load_dotenv()

import secrets
class Config:
    SQLALCHEMY_DATABASE_URI ="postgresql://app_rw_ffeh3f4asvt3n576ud3uhtv6eu:aX6ze2rkXyahkkzhPaIuApPNUxQOUBRr@pg-tunnel.borealis-data.com:53667/ddbc456cl5kqp3a5wo27kq7ulny"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'eaec3b4bd5ec5c8bab87ee8708f8217f'
    MAIL_SERVER = os.getenv('SMTP_SERVER')
    MAIL_PORT = os.getenv('SMTP_PORT')
    MAIL_USERNAME = os.getenv('SMTP_USERNAME')
    MAIL_PASSWORD = os.getenv('SMTP_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    