import psycopg2
import sys
sys.path.append("..")
#This function will be able to create a connection to the database. It will be called everytime a connection 
# is asked for and should return a connection to the database as and when requested. 
def db_connection(db_name):
    conn = psycopg2.connect(host='project-database-1',   #change to project-database-1
                            database=db_name,
                            user='gourav' ,    #os.environ['DB_USERNAME'],
                            password='gourav')         #os.environ['DB_PASSWORD'])
    return conn
    