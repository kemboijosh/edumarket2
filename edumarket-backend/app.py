import base64
import requests
import json
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
# Replace with your actual Safaricom Daraja credentials
CONSUMER_KEY = "u7GrXbRCyrmk4xZpIcnPZ42iZXzGSlp3WRA2BBaJpva5y86J"
CONSUMER_SECRET = "qHl3shBg4AJeL57fbGle2AUPMxTXnxGyJaUErSoZdLo6ocH28SHrr8kh1af69ttd"
PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
SHORTCODE = "174379"  # Sandbox Shortcode

# URLs
AUTH_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
STK_PUSH_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
NGROK_URL = "https://noncultivable-glazily-riley.ngrok-free.dev"

# --- MOCK DATABASES ---
users = []
products = [
    {"id": 1, "name": "Kiswahili Form 1 Textbook", "price": 650, "img": "https://source.unsplash.com/collection/education/300x150?sig=1"},
    {"id": 2, "name": "Geometry Set", "price": 350, "img": "https://source.unsplash.com/collection/education/300x150?sig=2"},
    {"id": 3, "name": "A4 Ruled Paper", "price": 200, "img": "https://source.unsplash.com/collection/education/300x150?sig=3"},
]

# --- HELPERS ---
def get_mpesa_access_token():
    """Get OAuth access token from Safaricom"""
    try:
        response = requests.get(
            AUTH_URL, 
            auth=(CONSUMER_KEY, CONSUMER_SECRET),
            headers={"Accept": "application/json"}
        )
        data = response.json()
        return data.get("access_token")
    except Exception as e:
        print(f"Error getting token: {e}")
        return None

def generate_password():
    """Generate Password and Timestamp for STK Push"""
    timestamp = time.strftime("%Y%m%d%H%M%S")
    data_to_encode = f"{SHORTCODE}{PASSKEY}{timestamp}"
    password = base64.b64encode(data_to_encode.encode()).decode("utf-8")
    return password, timestamp

# --- ROUTES ---
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not all([username, email, password]):
        return jsonify({"message": "All fields required"}), 400
    users.append({"username": username, "email": email, "password": password})
    return jsonify({"message": "Signup successful! Please login."}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user = next((u for u in users if u['email'] == email and u['password'] == password), None)
    if user:
        return jsonify({"user": {"username": user['username'], "email": user['email']}})
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.json
    name = data.get('name')
    price = data.get('price')
    img = data.get('img')
    new_id = max([p['id'] for p in products], default=0) + 1
    products.append({"id": new_id, "name": name, "price": float(price), "img": img})
    return jsonify({"message": "Product added"}), 201

# --- MPESA PAYMENT ---
@app.route('/pay', methods=['POST'])
def initiate_payment():
    data = request.json
    phone = data.get('phone')
    product_id = data.get('product_id')

    if not phone:
        return jsonify({"error": "Phone number is required"}), 400

    # Get product price
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    amount = product['price']

    # 1. Get Access Token
    access_token = get_mpesa_access_token()
    if not access_token:
        return jsonify({"error": "Failed to connect to payment provider"}), 500

    # 2. Generate Password & Timestamp
    password, timestamp = generate_password()

    # 3. Prepare STK Push Payload
    callback_url = f"{NGROK_URL}/callback"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": callback_url,
        "AccountReference": "EduMarket",
        "TransactionDesc": f"Payment for {product['name']}"
    }

    # 4. Send Request to Safaricom
    try:
        response = requests.post(STK_PUSH_URL, json=payload, headers=headers)
        res_data = response.json()
        
        print("Safaricom Response:", res_data)

        if "ResponseCode" in res_data and res_data["ResponseCode"] == "0":
            return jsonify({
                "success": True, 
                "message": "STK Push sent. Check your phone.",
                "MerchantRequestID": res_data.get("MerchantRequestID")
            })
        else:
            error_msg = res_data.get("errorMessage", "Payment request failed")
            return jsonify({"error": error_msg}), 400

    except Exception as e:
        print("Error during STK Push:", str(e))
        return jsonify({"error": "Server error processing payment"}), 500
@app.route('/callback', methods=['POST'])
def callback():
    """Safaricom STK Push callback"""
    data = request.json
    print("------- CALLBACK RECEIVED -------")
    print(json.dumps(data, indent=4))
    # ResultCode 0 = success
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)