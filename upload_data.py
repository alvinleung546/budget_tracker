from flask import jsonify
import pandas as pd
import sqlite3

def upload_file(request):
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    filename = file.filename.lower()

    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(file)
            return select_columns_from_csv(df)
        
        else:
            return jsonify({"error": "Unsupported file type"}), 400
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def select_columns_from_csv(df: pd.DataFrame):
    columns_to_keep = ["TRANSACTION DATE", "DESCRIPTION", "AMOUNT", "CATEGORY"]
    existing_columns = [col for col in columns_to_keep if col in df.columns]
    df = df[existing_columns]
    return create_transactions_from_csv(df)

def create_transactions_from_csv(df: pd.DataFrame):
    for row in df.values:
        row_list = list(row)
        insert_transaction_to_db(row_list)
    return jsonify({"success": "data uploaded"}), 200

def insert_transaction_to_db(data: list):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transactions (transaction_date, description, amount, category) VALUES (?, ?, ?, ?)", data)
        conn.commit()