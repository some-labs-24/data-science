from dotenv import load_dotenv
from datetime import datetime
import psycopg2
import os

def save_to_db(twitter_handle, json_string):
    twitter_handle = twitter_handle.lower()

    load_dotenv() 
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")

    current_date = datetime.now().strftime("%m/%d/%Y")

    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS results (
        id SERIAL PRIMARY KEY,
        twitter_handle varchar,
        date varchar,
        results jsonb
    );
    """
    cursor.execute(query)
    connection.commit()

    query = "SELECT * FROM results WHERE twitter_handle = '{}' ".format(twitter_handle)
    cursor.execute(query)

    if len(cursor.fetchall()) == 1:
        query = """
        UPDATE results
        SET
            date = '{}',
            results = '{}'
        WHERE twitter_handle = '{}';
        """.format(current_date, json_string, twitter_handle)
        cursor.execute(query)
    else:
        query = """
        INSERT INTO results (twitter_handle, date, results)
        VALUES ('{}', '{}', '{}');
        """.format(twitter_handle, current_date, json_string)
        cursor.execute(query)

    connection.commit()
    connection.close()

    