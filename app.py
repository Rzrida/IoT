from flask import Flask, request
import sqlite3
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("7609060973:AAElNlWrSIY-160ofQPkA5ScxtULVPj84TM")

# Database
conn = sqlite3.connect("contacts.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    username TEXT,
    chat_id TEXT UNIQUE
)
""")
conn.commit()

@app.route("/")
def home():
    return "Bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if "message" in data:
        chat = data["message"]["chat"]
        chat_id = chat["id"]
        name = chat.get("first_name", "")
        username = chat.get("username", "")

        cur.execute(
            "INSERT OR IGNORE INTO contacts (name, username, chat_id) VALUES (?, ?, ?)",
            (name, username, chat_id)
        )
        conn.commit()

    return "ok"
