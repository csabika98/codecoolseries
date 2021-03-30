import psycopg2
import psycopg2.extras
import os


def get_connection_data(db_name=None):
    """
    Give back a properly formatted dictionary based on the environment variables values which are started
    with :MY__PSQL_: prefix

    :db_name: optional parameter. By default it uses the environment variable value.
    """
    if db_name is None:
        db_name = os.environ.get('MY_PSQL_DBNAME')

    return {
        'dbname': db_name,
        'user': os.environ.get('MY_PSQL_USER'),
        'host': os.environ.get('MY_PSQL_HOST'),
        'password': os.environ.get('MY_PSQL_PASSWORD')
    }


def check_for_email(connection_data=None):
    if connection_data is None:
        connection_data = get_connection_data()
    connect_str = "dbname={} user={} host={} password={}".format(connection_data['dbname'],
                                                                     connection_data['user'],
                                                                     connection_data['host'],
                                                                     connection_data['password'])
    connection = psycopg2.connect(connect_str)
    cursor = connection.cursor()
    cursor.execute(""" SELECT email FROM accounts ORDER BY id DESC;""")
    db_users = cursor.fetchall()
    email = []

    for i in range(len(db_users)):
        person = db_users[i][0]
        email.append(person)

    connection.commit()
    cursor.close()
    connection.close()

    return email


def check_for_username(connection_data=None):
    if connection_data is None:
        connection_data = get_connection_data()
    connect_str = "dbname={} user={} host={} password={}".format(connection_data['dbname'],
                                                                     connection_data['user'],
                                                                     connection_data['host'],
                                                                     connection_data['password'])
    connection = psycopg2.connect(connect_str)
    cursor = connection.cursor()
    cursor.execute(""" SELECT username FROM accounts ORDER BY id DESC;""")
    db_users = cursor.fetchall()
    users = []

    for i in range(len(db_users)):
        person = db_users[i][0]
        users.append(person)

    connection.commit()
    cursor.close()
    connection.close()

    return users


