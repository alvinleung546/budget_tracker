from flask import Flask, request, render_template
from flask_cors import CORS
import sqlite3
import upload_data


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                user_id INTEGER DEFAULT 1,
                transaction_date TEXT,
                description TEXT,
                amount REAL,
                category TEXT,
                predicted_category TEXT,
                predicted_confience REAL
            )
        ''')
        conn.commit()

@app.route('/')
def home():
    return render_template('app.html')

@app.route('/app/upload')
def app_upload():
    return render_template('upload.html')

@app.route("/api/upload", methods=["POST"])
def api_upload():
    if request.method == 'POST':
        return upload_data.upload_file(request)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)