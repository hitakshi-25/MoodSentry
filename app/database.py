# SQLAlchemy setup
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def get_db():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", 5432)  # default PostgreSQL port
    )
    return conn

def save_notification(user_id, message):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO notifications (user_id, message) VALUES (%s, %s)",
        (user_id, message)
    )
    db.commit()
    cursor.close()
    db.close()
