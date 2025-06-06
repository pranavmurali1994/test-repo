# db.py

import pyodbc
from config import SQL_SERVER, SQL_DATABASE, SQL_USERNAME, SQL_PASSWORD, SQL_DRIVER

def get_connection():
    conn_str = (
        f"DRIVER={SQL_DRIVER};"
        f"SERVER={SQL_SERVER};"
        f"DATABASE={SQL_DATABASE};"
        f"UID={SQL_USERNAME};"
        f"PWD={SQL_PASSWORD}"
    )
    return pyodbc.connect(conn_str)

def insert_metadata(filename, url):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO files (filename, url) VALUES (?, ?)", (filename, url))
    conn.commit()
    cursor.close()
    conn.close()
