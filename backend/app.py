import os
from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "database"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "appuser"),
        password=os.environ["DB_PASSWORD"],
        database=os.getenv("DB_NAME", "studentdb"),
        connection_timeout=3,
    )

@app.get("/api/health")
def health():
    try:
        conn = get_connection()
        conn.ping(reconnect=False, attempts=1, delay=0)
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except (Error, KeyError, ValueError):
        return jsonify({"status": "not_ready", "database": "unavailable"}), 503

@app.get("/api/students")
def students():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, course FROM students ORDER BY id")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows)
    except (Error, KeyError, ValueError):
        app.logger.exception("Unable to retrieve students")
        return jsonify({"error": "Database temporarily unavailable"}), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
