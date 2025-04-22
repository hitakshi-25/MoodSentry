# SQLAlchemy setup
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )

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
