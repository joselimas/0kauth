import sqlite3

def get_permitted_users():
    with sqlite3.connect('db/auth.db') as conn:
        c=conn.cursor()
        query=c.execute("select * from users where username='get_flag';")
        return {user:[int(salt,16),int(secret,16)] for salt,user,secret in query.fetchall()}
