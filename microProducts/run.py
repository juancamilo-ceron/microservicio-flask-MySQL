from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="myflaskapp"
    )

@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return jsonify(products)

@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, description, price, stock) VALUES (%s, %s, %s, %s)",
                   (data['name'], data.get('description', ''), data['price'], data['stock']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Product created"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
