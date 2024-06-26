from src.database import SessionLocal
import pika

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def get_msg_brocker_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    try:
        yield connection.channel()
    finally:
        connection.close() 