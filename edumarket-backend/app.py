import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# ── Database ──
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or 'sqlite:///edumarket.db'
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
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'img': self.img
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }


# ── Serve index.html at root ──
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


# ── Health Check ──
@app.route('/api/health')
def health():
    try:
        db.session.execute(db.text('SELECT 1'))
        return jsonify({"status": "healthy", "database": "connected"})
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


# ── Products ──
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return jsonify([p.to_dict() for p in products])


@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    if not data or not data.get('name') or data.get('price') is None:
        return jsonify({"error": "Name and price are required"}), 400

    product = Product(
        name=data['name'],
        price=float(data['price']),
        img=data.get('img', '')
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201


# ── Auth ──
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"message": "All fields are required"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already registered"}), 409

    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Signup successful!"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Email and password required"}), 400

    user = User.query.filter_by(email=data['email'], password=data['password']).first()
    if not user:
        return jsonify({"message": "Invalid email or password"}), 401

    return jsonify({"user": user.to_dict()})


# ── M-Pesa Mock Payment ──
@app.route('/pay', methods=['POST'])
def pay():
    data = request.get_json()
    phone = data.get('phone', '')
    product_id = data.get('product_id')

    if not phone or len(phone) < 10:
        return jsonify({"success": False, "error": "Enter a valid phone number"})

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"success": False, "error": "Product not found"})

    # In production, integrate with Safaricom Daraja API here
    return jsonify({
        "success": True,
        "message": f"M-Pesa prompt sent to {phone} for {product.name} (KES {product.price})"
    })


# ── Seed some sample products on first run ──
def seed_products():
    if Product.query.count() == 0:
        samples = [
            {"name": "Longhorn Mathematics Form 1", "price": 650, "img": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&q=80"},
            {"name": "Oxford English Dictionary", "price": 1200, "img": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400&q=80"},
            {"name": "Premium Geometry Set", "price": 350, "img": "https://images.unsplash.com/photo-1586495985370-7866e10d1a82?w=400&q=80"},
            {"name": "Crayola Color Pencils (36pc)", "price": 850, "img": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400&q=80"},
            {"name": "A4 Exercise Books (10 Pack)", "price": 500, "img": "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=400&q=80"},
            {"name": "Scientific Calculator CX-991", "price": 1800, "img": "https://images.unsplash.com/photo-1612170153139-6f881ff067e8?w=400&q=80"},
            {"name": "Atlas Notebook A5 (Hardcover)", "price": 280, "img": "https://images.unsplash.com/photo-1528938102132-4a9276b8e320?w=400&q=80"},
            {"name": "Staedtler Fineliners (10 Colors)", "price": 950, "img": "https://images.unsplash.com/photo-1585336261022-680e295ce3fe?w=400&q=80"},
        ]
        for s in samples:
            db.session.add(Product(**s))
        db.session.commit()


with app.app_context():
    db.create_all()
    seed_products()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)