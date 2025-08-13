from flask import Flask, request
import os
import sqlite3

app = Flask(__name__)


@app.route("/user")
def get_user():
    username = request.args.get("name")
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE name = '{username}'"  
    cursor.execute(query)
    result = cursor.fetchall()
    return {"users": result}

@app.route("/")
def hello():
    return "Hello from Vulnerable Flask App!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
