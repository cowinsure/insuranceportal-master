
# utils/db.py
# DB Connection Utility for Django Web API
import psycopg2
from django.conf import settings

def get_db_connection():
    db = settings.DATABASES['default']
    return psycopg2.connect(
        dbname=db['NAME'],
        user=db['USER'],
        password=db['PASSWORD'],
        host=db['HOST'],
        port=db['PORT'],
    )

# Function to call a database function with parameters
# This function executes a database function and returns the results as a list of dictionaries.
def call_db_function(conn, function_name, params=()):
    with conn.cursor() as cursor:
        query = f"SELECT * FROM {function_name}({','.join(['%s'] * len(params))})"
        cursor.execute(query, params)
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]