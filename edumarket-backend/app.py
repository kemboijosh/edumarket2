import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

# Get the folder where app.py lives — works on Render, local, everywhere
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')
CORS(app)

# ── Database ──
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

if not DATABASE_URL:
    db_path = os.path.join(os.environ.get('TMPDIR', '/tmp'), 'edumarket.db')
    DATABASE_URL = 'sqlite:///' + db_path

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# ── Models ──
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    img = db.Column(db.String(500), default='')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'price': self.price, 'img': self.img}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}


# ── Serve index.html ──
@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')


# ── Health Check ──
@app.route('/api/health')
def health():
    try:
        db.session.execute(db.text('SELECT 1'))
        product_count = Product.query.count()
        return jsonify({"status": "healthy", "database": "connected", "products": product_count})
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


# ── Products ──
@app.route('/products', methods=['GET'])
def get_products():
    try:
        products = Product.query.order_by(Product.created_at.desc()).all()
        return jsonify([p.to_dict() for p in products])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/add_product', methods=['POST'])
def add_product():
    try:
        data = request.get_json()
        if not data or not data.get('name') or data.get('price') is None:
            return jsonify({"error": "Name and price are required"}), 400
        product =