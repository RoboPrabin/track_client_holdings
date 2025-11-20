import psycopg2
import psycopg2.extras

def get_connection():
    return psycopg2.connect(
        host="localhost",
        dbname="client_holdings",
        user="postgres",
        password="admin",
        cursor_factory=psycopg2.extras.DictCursor
    )

def get_user_by_username(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM app_user WHERE username = %s", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row
