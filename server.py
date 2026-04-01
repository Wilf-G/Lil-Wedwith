from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app) # Allows your website to talk to this script

def init_db():
    conn = sqlite3.connect('food_inc.db')
    cursor = conn.cursor()
    # Create Orders Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
         customer_name TEXT, 
         service_type TEXT, 
         location TEXT, 
         total_price REAL,
         status TEXT DEFAULT 'Pending',
         timestamp DATETIME)''')
    # Create Order Items Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS order_items 
        (order_id INTEGER, item_name TEXT, quantity INTEGER)''')
    # Create Stock Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS stock 
        (item_name TEXT PRIMARY KEY, quantity INTEGER)''')
    
    # Initialize some dummy stock
    cursor.execute("INSERT OR IGNORE INTO stock VALUES ('Burger', 50), ('Pizza', 30), ('Wraps', 40), ('Pasta', 25)")
    conn.commit()
    conn.close()

@app.route('/api/order', methods=['POST'])
def save_order():
    data = request.json
    conn = sqlite3.connect('food_inc.db')
    cursor = conn.cursor()
    
    # Save Main Order
    cursor.execute("INSERT INTO orders (customer_name, service_type, location, total_price, timestamp) VALUES (?, ?, ?, ?, ?)",
                   (data['name'], data['type'], data['location'], data['total'], datetime.now()))
    order_id = cursor.lastrowid
    
    # Save Items and Deduct Stock
    for item in data['items']:
        cursor.execute("INSERT INTO order_items VALUES (?, ?, ?)", (order_id, item['name'], item['qty']))
        cursor.execute("UPDATE stock SET quantity = quantity - ? WHERE item_name LIKE ?", (item['qty'], f"%{item['name']}%"))
    
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "order_id": order_id})

if __name__ == '__main__':
    init_db()
    app.run(port=5000, debug=True)