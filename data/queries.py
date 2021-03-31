from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')

#CONVERT SQL QUERY TO JSON!
def most_rated_show(page_number):
    return data_manager.execute_select("""
    SELECT json_agg(t)
    FROM (
    SELECT (shows.id) as id, title,year,rating,trailer,homepage,runtime,ARRAY_AGG (name) genres
    FROM shows
    INNER JOIN show_genres ON (shows.id = show_genres.show_id)
    INNER JOIN genres ON(show_genres.genre_id = genres.id)
    GROUP BY shows.id,title,year,rating,trailer,homepage,runtime
    ORDER BY
    shows.rating DESC
    LIMIT
    15
    OFFSET (%(Page_number)s -1)*15) t
    """, variables={"Page_number":page_number})

def overview(show_id:str):
    return data_manager.execute_select('SELECT shows.id, shows.title, shows.runtime, shows.overview, shows.trailer, shows.homepage, shows.year, shows.rating FROM shows WHERE id = %s', (show_id,))

def seasonoverview(show_id:str):
    return data_manager.execute_select("SELECT id, title, overview FROM seasons WHERE show_id = %s", (show_id,))

def register(username:str, email:str, password:str, created_on:str) -> list:
    return data_manager.modify_database("INSERT INTO accounts(username,email,password,createdon) VALUES(%s,%s,%s,%s)", (username, email,password,created_on))

def get_email_and_password(email:str, password:str):
    return data_manager.execute_select("SELECT email, password FROM accounts WHERE email=%s AND password=%s",(email, password))

def rewrite_password(password:str, email:str) ->list:
    return data_manager.modify_database("UPDATE accounts SET password =%s WHERE email=%s",(password,email))

def login_user(email):
    return data_manager.execute_select("SELECT email, password FROM accounts WHERE (email=%(email)s);",variables={'email':email})

def list_emails():
    return data_manager.execute_select("SELECT email from accounts")

def list_usernames():
    return data_manager.execute_select("SELECT username from accounts")