import os 
from dotenv import load_dotenv
import MySQLdb

load_dotenv()

def connexion():
    mysql = MySQLdb.connect(
        host= os.getenv('MYSQL_HOST'),
        user= os.getenv('MYSQL_USER'),
        passwd= os.getenv('MYSQL_PASSWORD'),
        db= os.getenv('MYSQL_DATABASE'),
        )
    return mysql

mysql = connexion()
