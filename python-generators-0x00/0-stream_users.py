#!/usr/bin/python3
import mysql.connector

def stream_users():
    """Generator that streams users row-by-row from the database"""

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="hqjfwkejfd",
        database="ALX_prodev"
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")

    for row in cursor:
        yield row  # Stream row by row

    cursor.close()
    connection.close()
