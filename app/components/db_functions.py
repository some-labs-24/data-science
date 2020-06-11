from dotenv import load_dotenv
from datetime import datetime
import psycopg2
import os


def get_db_connection():
    """
    Starts a connection to the AWS database and returns the connection object.
    """
    load_dotenv()

    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)

    return connection


def save_model_results(twitter_handle, json_string):
    """
    Saves a model result (in the form of a json string) to the database.
    """
    twitter_handle = twitter_handle.lower()

    current_date = datetime.now().strftime("%m/%d/%Y")

    connection = get_db_connection()
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


def get_model_results(twitter_handle):
    """
    Returns model results from database in the form of a dictionary.
    """
    twitter_handle = twitter_handle.lower()
    connection = get_db_connection()
    cursor = connection.cursor()

    query = "SELECT results FROM results WHERE twitter_handle = '{}';".format(twitter_handle)
    cursor.execute(query)
    data = cursor.fetchone()[0]
    connection.close()
    return data


def is_name_in_queue(twitter_handle):
    """
    Returns True if a twitter handle is on the queue list.
    """
    twitter_handle = twitter_handle.lower()
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS queue (
        id SERIAL PRIMARY KEY,
        twitter_handle varchar
    );
    """
    cursor.execute(query)
    connection.commit()

    query = """
    SELECT EXISTS(SELECT 1 FROM queue WHERE twitter_handle='{}');
    """.format(twitter_handle)
    cursor.execute(query)
    name_exists = cursor.fetchall()[0][0]
    connection.close()
    return name_exists


def is_name_in_processing(twitter_handle):
    """
    Returns True if a twitter handle is on the processing list.
    """
    twitter_handle = twitter_handle.lower()
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS processing (
        id SERIAL PRIMARY KEY,
        twitter_handle varchar
    );
    """
    cursor.execute(query)
    connection.commit()

    query = """
    SELECT EXISTS(SELECT 1 FROM processing WHERE twitter_handle='{}');
    """.format(twitter_handle)
    cursor.execute(query)
    name_exists = cursor.fetchall()[0][0]
    connection.close()
    return name_exists


def is_model_ready(twitter_handle):
    """
    Returns true if a twitter handle is on the results list.
    """
    twitter_handle = twitter_handle.lower()
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS results (
        id SERIAL PRIMARY KEY,
        twitter_handle varchar
    );
    """
    cursor.execute(query)
    connection.commit()

    query = """
    SELECT EXISTS(SELECT 1 FROM results WHERE twitter_handle='{}');
    """.format(twitter_handle)
    cursor.execute(query)
    name_exists = cursor.fetchall()[0][0]
    connection.close()
    return name_exists


def add_name_to_queue(twitter_handle):
    """
    Adds name to queue list in database.
    """
    twitter_handle = twitter_handle.lower()
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS queue (
        id SERIAL PRIMARY KEY,
        twitter_handle varchar
    );
    """
    cursor.execute(query)
    connection.commit()

    query = """
    INSERT INTO queue (twitter_handle)
    VALUES ('{}');
    """.format(twitter_handle)
    cursor.execute(query)
    connection.close()


def move_to_processing(twitter_handle):
    """
    Removes a name from the queue and moves it to processing.
    """
    twitter_handle = twitter_handle.lower()
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS processing (
        id SERIAL PRIMARY KEY,
        twitter_handle varchar
    );
    """
    cursor.execute(query)
    connection.commit()

    query = """
    DELETE FROM queue
    WHERE twitter_handle = '{}';
    """.format(twitter_handle)
    cursor.execute(query)
    connection.commit()

    query = """
    INSERT INTO processing (twitter_handle)
    VALUES ('{}');
    """.format(twitter_handle)
    cursor.execute(query)
    connection.commit()
    connection.close()


def remove_from_processing(twitter_handle):
    """
    Removes a name from the processing list in the database.
    """
    twitter_handle = twitter_handle.lower()
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    DELETE FROM processing
    WHERE twitter_handle = '{}';
    """.format(twitter_handle)
    cursor.execute(query)
    connection.commit()
    connection.close()


def is_name_in_engagement(twitter_handle):
    """
    Returns True if a user already has engagement data in the database.
    """
    twitter_handle = twitter_handle.lower()
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS engagement (
        twitter_handle VARCHAR PRIMARY KEY,
        num_followers INT,
        num_retweets INT,
        num_likes INT,
        engagement_ratio FLOAT
    );
    """
    cursor.execute(query)
    connection.commit()

    query = """
    SELECT EXISTS(SELECT 1 FROM engagement WHERE twitter_handle='{}');
    """.format(twitter_handle)
    cursor.execute(query)
    name_exists = cursor.fetchall()[0][0]
    connection.close()
    return name_exists


def update_engagement(twitter_handle, num_followers, num_retweets, num_likes, engagement_ratio):
    """
    Updates the engagement table in the database.
    """
    twitter_handle = twitter_handle.lower()
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS engagement (
        twitter_handle VARCHAR PRIMARY KEY,
        num_followers INT,
        num_retweets INT,
        num_likes INT,
        engagement_ratio FLOAT
    );
    """
    cursor.execute(query)
    connection.commit()

    query = """
    INSERT INTO engagement
    VALUES ('{}', {}, {}, {}, {})
    ON CONFLICT (twitter_handle) DO UPDATE
    SET num_followers={}, num_retweets={}, num_likes={}, engagement_ratio={};
    """.format(twitter_handle, num_followers, num_retweets, num_likes, engagement_ratio,
               num_followers, num_retweets, num_likes, engagement_ratio)

    cursor.execute(query)
    connection.commit()
    connection.close()


def get_engagement(twitter_handle):
    """
    Returns the engagement data in dictionary form from the database.
    """
    twitter_handle = twitter_handle.lower()
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    SELECT * from engagement
    WHERE twitter_handle = '{}';
    """.format(twitter_handle)
    cursor.execute(query)
    data = cursor.fetchall()[0]
    connection.close()

    return {
        'num_followers': data[1],
        'num_retweets': data[2],
        'num_favorites': data[3],
        'engagement_ratio': data[4]
    }


if __name__ == "__main__":
    print(is_model_ready('dutchbros'))
    print(is_name_in_processing('dutchbros'))
