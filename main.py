import sqlite3
import uuid
import random
from datetime import datetime, timedelta
from flask import Flask, request, jsonify

app = Flask(__name__)
DATABASE_NAME = 'report_configurations.db'


def setup_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id TEXT PRIMARY KEY
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UserActivity (
            user_id TEXT NOT NULL,
            online_time INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES Users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ReportsConfiguration (
            report_name TEXT PRIMARY KEY,
            metrics TEXT NOT NULL,
            user_ids TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def seed_data():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM Users')
    cursor.execute('DELETE FROM UserActivity')
    cursor.execute('DELETE FROM ReportsConfiguration')

    user_ids = [str(uuid.uuid4()) for _ in range(10)]
    cursor.executemany('INSERT INTO Users (id) VALUES (?)', [(user_id,) for user_id in user_ids])

    today = datetime.now().date()
    for user_id in user_ids:
        for days_ago in range(15):
            date = today - timedelta(days=days_ago)
            online_time = random.randint(10, 86400)
            cursor.execute('INSERT INTO UserActivity (user_id, online_time, date) VALUES (?, ?, ?)',
                           (user_id, online_time, date.isoformat()))

    example_reports = [
        ('report1', 'dailyAverage,total,weeklyAverage', ','.join(user_ids[:5])),
        ('report2', 'max,min', ','.join(user_ids[5:])),
    ]
    cursor.executemany('INSERT INTO ReportsConfiguration (report_name, metrics, user_ids) VALUES (?, ?, ?)',
                       example_reports)

    conn.commit()
    conn.close()


@app.route("/api/reports", methods=['GET'])
def get_reports_list():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT report_name, metrics, user_ids FROM ReportsConfiguration')
    reports = cursor.fetchall()
    response = []

    for report_name, metrics, user_ids in reports:
        report_data = {
            "name": report_name,
            "metrics": metrics.split(','),
            "users": user_ids.split(',')
        }
        response.append(report_data)

    conn.close()
    return jsonify(response)


if __name__ == '__main__':
    setup_database()
    seed_data()
    app.run(debug=True)

