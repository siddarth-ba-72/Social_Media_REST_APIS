import os
from flask import Flask, request, render_template
import psycopg2
from dotenv import load_dotenv
from datetime import datetime, timezone
from db_sql_queries import *


load_dotenv()

app = Flask(__name__, template_folder='templates')
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)


# Post a new message
@app.post('/api/new/message')
def new_message():
    data = request.get_json()
    text = data["message"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_MESSAGES_TABLE)
            cursor.execute(ADD_MESSAGE_TO_TABLE, (
                text,
            ))
            msg = cursor.fetchone()[0]
    return {
        "text": msg,
        "status": f"Message added successfully"
    }, 201


# View all messages
@app.get("/api/all/messages")
def view_all_messages():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(VIEW_ALL_MESSAGES)
            messages = cursor.fetchall()
    return {
        "messages": messages
    }, 201


# Total number of likes for each message
@app.get('/api/likes/messages')
def no_of_likes_for_each_message():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_LIKES_TABLE)
            cursor.execute(LIST_ALL_MESSAGES_WITH_LIKES)
            messages = cursor.fetchall()
    likes_per_message = {}
    for msg in messages:
        likes_per_message[msg[0]] = msg[1]
    return render_template('likePerMsg.html', likes_per_message=likes_per_message)
    # return {
    #     "Likes per Message": likes_per_message
    # }, 201


# Liking a message
@app.post("/api/like/msg")
def like_message():
    data = request.get_json()
    message_id = data["message_id"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(LIKE_A_MESSAGE, (
                message_id,
            ))
    return {
        "status": "Message liked successfully",
    }, 201


# Unlike a message
@app.post("/api/unlike/msg")
def unlike_message():
    data = request.get_json()
    message_id = data["message_id"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UNLIKE_A_MESSAGE, (
                message_id, message_id
            ))
    return {
        "status": "Message unliked successfully",
    }, 201
