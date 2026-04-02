import os
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
if not DATABASE_URL:
    db_path = os.path.join(os.environ.get('TMPDIR', '/tmp'), 'edumarket.db')
    DATABASE_URL = 'sqlite:///' + db_path

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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


HTML_PAGE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<title>EduMarket - Stationery &amp; Books</title>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&amp;display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
<style>
:root{--primary:#4f46e5;--primary-dark:#3730a3;--secondary:#0d9488;--bg-light:#f8fafc;--text-dark:#1e293b;--text-light:#64748b;--white:#fff;--danger:#ef4444;--success:#22c55e;--accent:#6366f1}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Poppins,sans-serif;background:var(--bg-light);color:var(--text-dark);line-height:1.6}
.nav{background:var(--white);padding:1rem 2rem;display:flex;justify-content:space-between;align-items:center;box-shadow:0 4px 8px rgba(0,0,0,.05);position:sticky;top:0;z-index:50}
.nav h2{color:var(--primary);font-weight:700;font-size:1.5rem;cursor:pointer;display:flex;align-items:center;gap:8px;transition:color .3s}
.nav h2:hover{color:var(--accent)}
.nav-links{display:flex;gap:1rem;align-items:center}
.nav-btn{padding:.5rem 1.2rem;border:2px solid var(--primary);background:0 0;color:var(--primary);font-weight:600;cursor:pointer;border-radius:8px;transition:all .3s;font-size:.95rem}
.nav-btn:hover{background:var(--primary);color:var(--white);box-shadow:0 4px 8px rgba(0,0,0,.1)}
.nav-btn.primary{background:var(--primary);color:var(--white)}
.nav-btn.primary:hover{background:var(--primary-dark);border-color:var(--primary-dark)}
.user-badge{background:var(--bg-light);padding:.5rem 1rem;border-radius:20px;font-size:.9rem;color:var(--text-dark);font-weight:600;display:flex;align-items:center;gap:8px;box-shadow:0 2px 4px rgba(0,0,0,.05)}
.hero{background:linear-gradient(135deg,var(--primary),var(--primary-dark));color:#fff;padding:4rem 2rem;text-align:center;margin-bottom:2rem;border-radius:8px;box-shadow:0 8px 16px rgba(0,0,0,.1)}
.hero h1{font-size:2.8rem;margin-bottom:1rem}
.hero p{font-size:1.2rem;opacity:.95;max-width:600px;margin:0 auto}
.carousel-wrapper{max-width:1200px;margin:0 auto 2rem;padding:0 2rem}
.carousel-container{position:relative;overflow:hidden;border-radius:16px;box-shadow:0 10px 20px rgba(0,0,0,.1)}
.carousel-slides{display:flex;transition:transform .6s cubic-bezier(.25,1,.5,1);height:400px}
.carousel-slide{min-width:100%;position:relative;background:linear-gradient(135deg,#e0e7ff,#c7d2fe)}
.carousel-slide img{width:100%;height:100%;object-fit:cover}
.carousel-slide .slide-fallback{width:100%;height:100%;display:none;align-items:center;justify-content:center;color:var(--primary);font-size:4rem;opacity:.4}
.carousel-caption{position:absolute;bottom:0;left:0;right:0;background:linear-gradient(to top,rgba(0,0,0,.8),transparent);color:#fff;padding:2rem;text-align:left}
.carousel-caption h3{font-size:1.8rem;margin-bottom:.5rem;text-shadow:0 2px 4px rgba(0,0,0,.5)}
.carousel-caption p{font-size:1rem;opacity:.9}
.carousel-btn{position:absolute;top:50%;transform:translateY(-50%);background:rgba(255,255,255,.8);color:var(--text-dark);border:none;width:50px;height:50px;border-radius:50%;font-size:1.2rem;cursor:pointer;transition:all .3s;z-index:10;display:flex;align-items:center;justify-content:center}
.carousel-btn:hover{background:#fff;box-shadow:0 4px 12px rgba(0,0,0,.2)}
.prev{left:20px}.next{right:20px}
.carousel-dots{position:absolute;bottom:20px;left:50%;transform:translateX(-50%);display:flex;gap:10px;z-index:10}
.dot{width:12px;height:12px;background:rgba(255,255,255,.5);border-radius:50%;cursor:pointer;transition:background .3s;border:2px solid transparent}
.dot.active{background:#fff;transform:scale(1.1)}
.container{max-width:1200px;margin:2rem auto;padding:0 2rem}
.section-header{margin-bottom:2rem;display:flex;justify-content:space-between;align-items:center}
.section-header h2{color:var(--text-dark);font-size:1.8rem;font-weight:600}
.products{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:2rem}
.card{background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 4px 12px rgba(0,0,0,.05);transition:transform .3s,box-shadow .3s;display:flex;flex-direction:column}
.card:hover{transform:translateY(-8px);box-shadow:0 20px 30px rgba(0,0,0,.15)}
.card-img-wrapper{width:100%;height:180px;overflow:hidden;background:linear-gradient(135deg,#e0e7ff,#c7d2fe);display:flex;align-items:center;justify-content:center}
.card-img-wrapper img{width:100%;height:100%;object-fit:cover;transition:transform .3s}
.card:hover .card-img-wrapper img{transform:scale(1.05)}
.card-img-wrapper .img-fallback{font-size:3rem;color:var(--primary);opacity:.5}
.card-body{padding:1.5rem;flex-grow:1;display:flex;flex-direction:column}
.card-title{font-size:1.3rem;font-weight:600;margin-bottom:.5rem}
.card-price{font-size:1.25rem;color:var(--secondary);font-weight:700;margin-bottom:1rem}
.card-btn{width:100%;padding:.75rem;margin-top:auto;background:linear-gradient(135deg,var(--primary),var(--accent));color:#fff;border:none;cursor:pointer;border-radius:8px;font-weight:600;font-size:.95rem;transition:all .3s}
.card-btn:hover{background:linear-gradient(135deg,var(--primary-dark),var(--accent));box-shadow:0 4px 12px rgba(0,0,0,.2)}
.modal-overlay{display:none;position:fixed;z-index:100;left:0;top:0;width:100%;height:100%;background:rgba(15,23,42,.6);backdrop-filter:blur(4px);justify-content:center;align-items:center;animation:fadeIn .3s}
.modal-content{background:#fff;padding:2.5rem;border-radius:16px;width:100%;max-width:400px;margin:1rem;position:relative;box-shadow:0 10px 20px rgba(0,0,0,.15)}
.close-modal{position:absolute;top:1rem;right:1rem;background:0 0;border:none;font-size:1.5rem;color:var(--text-light);cursor:pointer;transition:color .3s}
.close-modal:hover{color:var(--primary)}
.modal-header{text-align:center;margin-bottom:1.5rem}
.modal-header h3{font-size:1.5rem;color:var(--text-dark);margin-bottom:.5rem}
.modal-header p{color:var(--text-light);font-size:.9rem}
.form-group{margin-bottom:1rem}
.form-input{width:100%;padding:.75rem 1rem;border:2px solid #e2e8f0;border-radius:8px;font-family:Poppins,sans-serif;font-size:.95rem;transition:border-color .3s,box-shadow .3s}
.form-input:focus{outline:none;border-color:var(--primary);box-shadow:0 0 8px rgba(79,70,229,.2)}
.modal-buttons{display:flex;flex-direction:column;gap:1rem;margin-top:1.5rem}
.btn-submit{background:linear-gradient(135deg,var(--primary),var(--accent));color:#fff;padding:.75rem;border:none;cursor:pointer;border-radius:8px;font-weight:600;font-size:1rem;transition:all .3s;font-family:Poppins,sans-serif;display:flex;align-items:center;justify-content:center;gap:8px}
.btn-submit:hover{background:linear-gradient(135deg,var(--primary-dark),var(--accent));box-shadow:0 4px 12px rgba(0,0,0,.2)}
.btn-submit:disabled{opacity:.6;cursor:not-allowed}
.btn-switch{background:0 0;color:var(--text-light);border:none;cursor:pointer;font-size:.9rem;font-family:Poppins,sans-serif}
.btn-switch:hover{text-decoration:underline;color:var(--primary)}
#toast{visibility:hidden;min-width:250px;background-color:#333;color:#fff;text-align:center;border-radius:8px;padding:16px;position:fixed;z-index:200;right:30px;bottom:30px;font-size:.9rem;box-shadow:0 4px 12px rgba(0,0,0,.15)}
#toast.show{visibility:visible;animation:slideIn .5s,fadeOut .5s 2.5s}
@keyframes slideIn{from{bottom:0;opacity:0}to{bottom:30px;opacity:1}}
@keyframes fadeOut{from{opacity:1}to{opacity:0}}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@keyframes spin{to{transform:rotate(360deg)}}
.loading-spinner{display:inline-block;width:18px;height:18px;border:2px solid rgba(255,255,255,.3);border-radius:50%;border-top-color:#fff;animation:spin .6s linear infinite;vertical-align:middle;margin-right:8px}
.loading-state{grid-column:1/-1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:4rem 2rem;gap:1rem;color:var(--text-light)}
.spinner{width:40px;height:40px;border:4px solid #e2e8f0;border-top-color:var(--primary);border-radius:50%;animation:spin .8s linear infinite}
.error-state{grid-column:1/-1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:4rem 2rem;gap:1rem;color:var(--text-light);text-align:center}
.error-state i{font-size:2.5rem;color:var(--danger);opacity:.6}
.retry-btn{padding:.6rem 1.5rem;background:var(--primary);color:#fff;border:none;border-radius:8px;font-weight:600;cursor:pointer;font-family:Poppins,sans-serif;font-size:.9rem;transition:all .3s;display:flex;align-items:center;gap:8px}
.retry-btn:hover{background:var(--primary-dark);box-shadow:0 4px 12px rgba(0,0,0,.15)}
.professional-footer{position:relative;background:linear-gradient(to bottom,#1e293b,#0f172a);border-top:1px solid #334155;margin-top:4rem}
.footer-glow-top{position:absolute;top:0;left:50%;transform:translateX(-50%);width:50%;height:1px;background:linear-gradient(to right,transparent,rgba(79,70,229,.5),transparent)}
.footer-glow-orb{position:absolute;top:0;left:50%;transform:translateX(-50%);width:24rem;height:8rem;background:rgba(79,70,229,.15);filter:blur(3rem)}
.footer-main{max-width:1200px;margin:0 auto;padding:4rem 2rem 2rem}
.footer-top{display:grid;grid-template-columns:1fr;gap:3rem;padding-bottom:3rem;border-bottom:1px solid rgba(100,116,139,.3)}
@media(min-width:1024px){.footer-top{grid-template-columns:1.2fr 2fr;gap:2rem}}
.footer-brand{display:flex;flex-direction:column;gap:1.5rem}
.footer-logo{display:inline-flex;align-items:center;gap:.5rem;text-decoration:none;transition:all .3s;width:fit-content;cursor:pointer}
.footer-logo:hover{transform:scale(1.02)}
.footer-logo-icon{width:2.5rem;height:2.5rem;background:var(--primary);border-radius:.5rem;display:flex;align-items:center;justify-content:center;transition:background .3s}
.footer-logo:hover .footer-logo-icon{background:var(--accent)}
.footer-logo-icon i{color:#fff;font-size:1.25rem}
.footer-logo-text{font-size:1.5rem;font-weight:600;color:#fff}
.footer-logo-text span{color:var(--primary)}
.footer-description{color:#94a3b8;font-size:.9rem;line-height:1.7;max-width:28rem}
.newsletter-title{color:#fff;font-size:.9rem;font-weight:500;margin-bottom:.75rem}
.newsletter-form{display:flex;gap:.5rem;flex-wrap:wrap}
.newsletter-input{flex:1;min-width:200px;padding:.75rem 1rem;background:rgba(30,41,59,.8);border:1px solid #334155;border-radius:.5rem;color:#fff;font-size:.875rem;font-family:Poppins,sans-serif;transition:all .3s}
.newsletter-input::placeholder{color:#64748b}
.newsletter-input:focus{outline:none;border-color:var(--primary);box-shadow:0 0 0 3px rgba(79,70,229,.2)}
.newsletter-btn{padding:.75rem 1.25rem;background:var(--primary);color:#fff;border:none;border-radius:.5rem;font-weight:500;font-size:.875rem;cursor:pointer;font-family:Poppins,sans-serif;transition:all .3s}
.newsletter-btn:hover{background:var(--accent);box-shadow:0 4px 12px rgba(79,70,229,.3)}
.newsletter-privacy{color:#64748b;font-size:.75rem;margin-top:.5rem}
.footer-links-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:2rem}
@media(min-width:768px){.footer-links-grid{grid-template-columns:repeat(4,1fr)}}
.footer-column h4{color:#fff;font-size:.85rem;font-weight:600;text-transform:uppercase;letter-spacing:.05em;margin-bottom:1rem}
.footer-column ul{list-style:none;padding:0;margin:0}
.footer-column li{margin-bottom:.75rem}
.footer-column a{color:#94a3b8;text-decoration:none;font-size:.875rem;display:inline-flex;align-items:center;gap:.5rem;transition:color .3s;cursor:pointer}
.footer-column a i{font-size:.6rem;color:#475569;transition:color .3s}
.footer-column a:hover{color:var(--primary)}
.footer-column a:hover i{color:var(--primary)}
.hiring-badge{margin-left:.25rem;padding:.125rem .5rem;font-size:.65rem;background:rgba(79,70,229,.2);color:var(--primary);border-radius:9999px}
.footer-stats{padding:2.5rem 0;border-bottom:1px solid rgba(100,116,139,.3)}
.stats-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:2rem}
@media(min-width:768px){.stats-grid{grid-template-columns:repeat(4,1fr)}}
.stat-item{text-align:center}
.stat-number{font-size:1.875rem;font-weight:700;color:#fff;margin-bottom:.25rem}
.stat-label{font-size:.875rem;color:#64748b}
.footer-bottom{padding-top:2rem;display:flex;flex-direction:column;align-items:center;gap:1.5rem}
@media(min-width:768px){.footer-bottom{flex-direction:row;justify-content:space-between}}
.footer-copyright{display:flex;flex-direction:column;align-items:center;gap:1rem}
@media(min-width:640px){.footer-copyright{flex-direction:row;gap:1.5rem}}
.copyright-text{color:#64748b;font-size:.875rem}
.secure-badge{display:flex;align-items:center;gap:.5rem;padding:.375rem .75rem;background:rgba(30,41,59,.6);border:1px solid rgba(100,116,139,.3);border-radius:.5rem}
.secure-badge i{color:var(--success);font-size:.875rem}
.secure-badge span{color:#94a3b8;font-size:.75rem}
.payment-methods{display:flex;align-items:center;gap:1rem}
.payment-label{color:#64748b;font-size:.7rem;text-transform:uppercase;letter-spacing:.05em}
.payment-icons{display:flex;align-items:center;gap:.5rem}
.payment-icon{width:2.5rem;height:1.5rem;background:rgba(30,41,59,.8);border-radius:.25rem;display:flex;align-items:center;justify-content:center;color:#fff;font-size:.75rem}
.social-links{display:flex;align-items:center;gap:.75rem}
.social-label{color:#64748b;font-size:.7rem;text-transform:uppercase;letter-spacing:.05em;display:none}
@media(min-width:640px){.social-label{display:block}}
.social-link{width:2.25rem;height:2.25rem;background:rgba(30,41,59,.8);border-radius:.5rem;display:flex;align-items:center;justify-content:center;color:#94a3b8;text-decoration:none;transition:all .3s}
.social-link:hover{background:var(--primary);color:#fff}
.social-link i{font-size:.875rem}
@media(max-width:640px){.hero h1{font-size:2rem}.hero p{font-size:1rem}.carousel-slides{height:260px}.carousel-caption h3{font-size:1.2rem}.nav{padding:.75rem 1rem}.nav h2{font-size:1.2rem}.nav-btn{padding:.4rem .8rem;font-size:.85rem}}
</style>
</head>
<body>
<div class="nav">
<h2 onclick="location.reload()"><i class="fas fa-book"></i> EduMarket</h2>
<div class="nav-links" id="nav-links"></div>
</div>
<div class="hero">
<h1>Stationery &amp; Textbooks</h1>
<p>Get the best learning materials and school supplies delivered to you.</p>
</div>
<div class="carousel-wrapper">
<div class="carousel-container">
<div class="carousel-slides" id="carousel-slides">
<div class="carousel-slide">
<img src="https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1400&amp;h=400&amp;fit=crop&amp;q=80" alt="Back to School" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
<div class="slide-fallback"><i class="fas fa-school"></i></div>
<div class="carousel-caption"><h3>Back to School Offers</h3><p>Get 20% off on all textbooks and stationery kits this season.</p></div>
</div>
<div class="carousel-slide">
<img src="https://images.unsplash.com/photo-1456735190827-d1262f71b8a3?w=1400&amp;h=400&amp;fit=crop&amp;q=80" alt="Art Supplies" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
<div class="slide-fallback"><i class="fas fa-palette"></i></div>
<div class="carousel-caption"><h3>Premium Art Supplies</h3><p>Unleash creativity with our new range of colors and brushes.</p></div>
</div>
<div class="carousel-slide">
<img src="https://images.unsplash.com/photo-1588702547923-7093a6c3ba33?w=1400&amp;h=400&amp;fit=crop&amp;q=80" alt="Digital Learning" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
<div class="slide-fallback"><i class="fas fa-laptop"></i></div>
<div class="carousel-caption"><h3>Digital Learning Aids</h3><p>Scientific calculators and educational tablets now in stock.</p></div>
</div>
</div>
<button class="carousel-btn prev" onclick="changeSlide(-1)"><i class="fas fa-chevron-left"></i></button>
<button class="carousel-btn next" onclick="changeSlide(1)"><i class="fas fa-chevron-right"></i></button>
<div class="carousel-dots" id="carousel-dots"></div>
</div>
</div>
<div class="container" id="products-section">
<div class="section-header">
<h2>Available Stock</h2>
<button class="nav-btn" onclick="openAddProduct()"><i class="fas fa-plus"></i> Add Product</button>
</div>
<div class="products" id="products-container"></div>
</div>
<div class="modal-overlay" id="modal">
<div class="modal-content">
<button class="close-modal" onclick="closeModal()">&amp;times;</button>
<div class="modal-header">
<h3 id="modal-title">Welcome Back</h3>
<p id="modal-desc">Login to continue</p>
</div>
<form onsubmit="event.preventDefault(); submitForm();">
<div class="form-group" id="username-group" style="display:none">
<input class="form-input" id="username" placeholder="Full Name"/>
</div>
<div class="form-group" id="email-group">
<input class="form-input" id="email" placeholder="Email Address" type="email"/>
</div>
<div class="form-group" id="password-group">
<input class="form-input" id="password" type="password" placeholder="Password"/>
</div>
<div class="form-group" id="prod-group" style="display:none">
<input class="form-input" id="prod-name" placeholder="Product Name (e.g. Math Book)"/>
<input class="form-input" id="prod-price" placeholder="Price (KES)" type="number" style="margin-top:10px"/>
<input class="form-input" id="prod-img" placeholder="Image URL (Optional)" style="margin-top:10px"/>
</div>
<div class="form-group" id="mpesa-group" style="display:none">
<input class="form-input" id="mpesa-phone" placeholder="M-Pesa Phone (e.g. 2547...)" type="tel"/>
</div>
<div class="modal-buttons">
<button type="submit" class="btn-submit" id="btn-submit-text">Login</button>
<button type="button" class="btn-switch" id="switch-btn" onclick="toggleAuthMode()"></button>
</div>
</form>
</div>
</div>
<div id="toast">Message</div>
<footer class="professional-footer">
<div class="footer-glow-top"></div>
<div class="footer-glow-orb"></div>
<div class="footer-main">
<div class="footer-top">
<div class="footer-brand">
<div class="footer-logo" onclick="window.scrollTo({top:0,behavior:'smooth'})">
<div class="footer-logo-icon"><i class="fas fa-graduation-cap"></i></div>
<span class="footer-logo-text">Edu<span>Market</span></span>
</div>
<p class="footer-description">Empowering learners worldwide with premium educational resources. Discover textbooks, stationery, and learning tools to accelerate your education journey.</p>
<div>
<p class="newsletter-title">Subscribe to our newsletter</p>
<form class="newsletter-form" onsubmit="event.preventDefault(); showToast('Thank you for subscribing!', 'success');">
<input type="email" class="newsletter-input" placeholder="Enter your email" required>
<button type="submit" class="newsletter-btn">Subscribe</button>
</form>
<p class="newsletter-privacy">Join 50,000+ learners. No spam, unsubscribe anytime.</p>
</div>
</div>
<div class="footer-links-grid">
<div class="footer-column"><h4>Products</h4><ul>
<li><a onclick="scrollToProducts()"><i class="fas fa-chevron-right"></i> Textbooks</a></li>
<li><a onclick="scrollToProducts()"><i class="fas fa-chevron-right"></i> Stationery</a></li>
<li><a onclick="scrollToProducts()"><i class="fas fa-chevron-right"></i> Art Supplies</a></li>
<li><a onclick="scrollToProducts()"><i class="fas fa-chevron-right"></i> Digital Tools</a></li>
<li><a onclick="scrollToProducts()"><i class="fas fa-chevron-right"></i> Bundles</a></li>
</ul></div>
<div class="footer-column"><h4>Company</h4><ul>
<li><a onclick="showToast('Coming soon','info')"><i class="fas fa-chevron-right"></i> About Us</a></li>
<li><a onclick="showToast('Coming soon','info')"><i class="fas fa-chevron-right"></i> Careers <span class="hiring-badge">Hiring</span></a></li>
<li><a onclick="showToast('Coming soon','info')"><i class="fas fa-chevron-right"></i> Blog</a></li>
<li><a onclick="showToast('Coming soon','info')"><i class="fas fa-chevron-right"></i> Press Kit</a></li>
<li><a onclick="showToast('Coming soon','info')"><i class="fas fa-chevron-right"></i> Partners</a></li>
</ul></div>
<div class="footer-column"><h4>Resources</h4><ul>
<li><a onclick="showToast('Coming soon','info')"><i class="fas fa-chevron-right"></i> Help Center</a></li>
<li><a onclick="showToast('Coming soon','info')"><i class="fas fa-chevron-right"></i> Community</a></li>
<li><a onclick="showToast('Coming soon','info')"><i class="fas fa-chevron-right"></i> Tutorials</a></li>
<li><a onclick="showToast('Coming soon','info')"><i class="fas fa-chevron-right"></i> Documentation</a></li>
<li><a onclick="showToast('Coming soon','info')"><i class="fas fa-chevron-right"></i> API Reference</a></li>
</ul></div>
<div class="footer-column"><h4>Legal</h4><ul>
<li><a onclick="showToast('Coming soon','info')"><i class="fas fa-chevron-right"></i> Terms of Service</a></li>
<li><a onclick="showToast('Coming soon','info')"><i class="fas fa-chevron-right"></i> Privacy Policy</a></li>
<li><a onclick="showToast('Coming soon','info')"><i class="fas fa-chevron-right"></i> Cookie Policy</a></li>
<li><a onclick="showToast('Coming soon','info')"><i class="fas fa-chevron-right"></i> Licensing</a></li>
<li><a onclick="showToast('Coming soon','info')"><i class="fas fa-chevron-right"></i> Refund Policy</a></li>
</ul></div>
</div>
</div>
<div class="footer-stats">
<div class="stats-grid">
<div class="stat-item"><div class="stat-number">50K+</div><div class="stat-label">Active Learners</div></div>
<div class="stat-item"><div class="stat-number">2,500+</div><div class="stat-label">Products Available</div></div>
<div class="stat-item"><div class="stat-number">180+</div><div class="stat-label">Countries Served</div></div>
<div class="stat-item"><div class="stat-number">4.9/5</div><div class="stat-label">Average Rating</div></div>
</div>
</div>
<div class="footer-bottom">
<div class="footer-copyright">
<p class="copyright-text">&amp;copy; 2026 EduMarket. All rights reserved.</p>
<div class="secure-badge"><i class="fas fa-shield-halved"></i><span>Secure Payments</span></div>
</div>
<div class="payment-methods">
<span class="payment-label">We accept:</span>
<div class="payment-icons">
<div class="payment-icon" title="M-Pesa"><i class="fas fa-mobile-screen"></i></div>
<div class="payment-icon" title="Visa"><i class="fab fa-cc-visa"></i></div>
<div class="payment-icon" title="Mastercard"><i class="fab fa-cc-mastercard"></i></div>
<div class="payment-icon" title="PayPal"><i class="fab fa-cc-paypal"></i></div>
</div>
</div>
<div class="social-links">
<span class="social-label">Follow us:</span>
<a href="#" class="social-link" onclick="event.preventDefault();showToast('Coming soon','info')"><i class="fab fa-x-twitter"></i></a>
<a href="#" class="social-link" onclick="event.preventDefault();showToast('Coming soon','info')"><i class="fab fa-linkedin-in"></i></a>
<a href="#" class="social-link" onclick="event.preventDefault();showToast('Coming soon','info')"><i class="fab fa-youtube"></i></a>
<a href="#" class="social-link" onclick="event.preventDefault();showToast('Coming soon','info')"><i class="fab fa-instagram"></i></a>
</div>
</div>
</div>
</footer>
<script>
var API="";
var mode="login";
var currentProductId=null;
var products=[];
document.addEventListener("DOMContentLoaded",function(){updateNavbar();initCarousel();loadProducts();document.getElementById("modal").addEventListener("click",function(e){if(e.target.id==="modal")closeModal()});document.addEventListener("keydown",function(e){if(e.key==="Escape"&&document.getElementById("modal").style.display==="flex")closeModal()})});
function scrollToProducts(){document.getElementById("products-section").scrollIntoView({behavior:"smooth"})}
function showToast(m,t){var toast=document.getElementById("toast");toast.innerText=m;if(t==="error")toast.style.backgroundColor="#ef4444";else if(t==="success")toast.style.backgroundColor="#22c55e";else toast.style.backgroundColor="#4f46e5";toast.className="show";clearTimeout(toast._tid);toast._tid=setTimeout(function(){toast.className=""},3000)}
function updateNavbar(){var nav=document.getElementById("nav-links");var user=JSON.parse(localStorage.getItem("user"));if(user){nav.innerHTML='<div class="user-badge"><i class="fas fa-user-circle"></i> '+(user.username||user.email)+'</div><button class="nav-btn" onclick="logout()"><i class="fas fa-sign-out-alt"></i> Logout</button>'}else{nav.innerHTML='<button class="nav-btn" onclick="openLogin()">Login</button><button class="nav-btn primary" onclick="openSignup()">Sign Up</button>'}}
function logout(){localStorage.removeItem("user");updateNavbar();showToast("Logged out successfully","info")}
function loadProducts(){var c=document.getElementById("products-container");c.innerHTML='<div class="loading-state"><div class="spinner"></div><span>Loading products...</span></div>';fetch(API+"/products").then(function(r){if(!r.ok)throw new Error("Server error "+r.status);return r.json()}).then(function(d){products=d;renderProducts()}).catch(function(){c.innerHTML='<div class="error-state"><i class="fas fa-exclamation-triangle"></i><span>Could not load products</span><button class="retry-btn" onclick="loadProducts()"><i class="fas fa-redo"></i> Try Again</button></div>'})}
function renderProducts(){var c=document.getElementById("products-container");c.innerHTML="";if(products.length===0){c.innerHTML='<p style="grid-column:1/-1;text-align:center;color:#64748b">No products available yet.</p>';return}for(var i=0;i<products.length;i++){var p=products[i];var n=p.name.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");var img=p.img?'<img src="'+p.img+'" alt="'+n+'" onerror="this.parentElement.innerHTML=\'<i class=fas fa-book-open img-fallback></i>\'">':'<i class="fas fa-book-open img-fallback"></i>';var card=document.createElement("div");card.className="card";card.innerHTML='<div class="card-img-wrapper">'+img+'</div><div class="card-body"><h3 class="card-title">'+n+'</h3><p class="card-price">KES '+Number(p.price).toLocaleString()+'</p><button class="card-btn">Buy Now</button></div>';(function(pid){card.querySelector(".card-btn").addEventListener("click",function(){buy(pid)})})(p.id);c.appendChild(card)}}
function buy(pid){if(!localStorage.getItem("user")){showToast("Please login to buy items","error");openLogin();return}currentProductId=pid;openPayModal()}
var slideIndex=1,autoSlideInterval;
function initCarousel(){var slides=document.querySelectorAll(".carousel-slide");var dc=document.getElementById("carousel-dots");for(var i=0;i<slides.length;i++){var d=document.createElement("span");d.className="dot";if(i===0)d.className="dot active";d.onclick=(function(idx){return function(){goToSlide(idx+1)}})(i);dc.appendChild(d)}showSlide(slideIndex);autoSlideInterval=setInterval(function(){advanceSlide(1)},5000)}
function advanceSlide(n){showSlide(slideIndex+=n)}
function goToSlide(n){showSlide(slideIndex=n)}
function showSlide(n){var slides=document.querySelectorAll(".carousel-slide");var dots=document.querySelectorAll(".dot");if(n>slides.length)slideIndex=1;if(n<1)slideIndex=slides.length;var c=document.getElementById("carousel-slides");if(c)c.style.transform="translateX(-"+((slideIndex-1)*100)+"%)";for(var i=0;i<dots.length;i++)dots[i].className="dot";if(dots[slideIndex-1])dots[slideIndex-1].className="dot active"}
function changeSlide(n){clearInterval(autoSlideInterval);advanceSlide(n);autoSlideInterval=setInterval(function(){advanceSlide(1)},5000)}
function resetModal(){document.getElementById("username-group").style.display="none";document.getElementById("prod-group").style.display="none";document.getElementById("mpesa-group").style.display="none";document.getElementById("email-group").style.display="block";document.getElementById("password-group").style.display="block";var inputs=document.querySelectorAll(".form-input");for(var i=0;i<inputs.length;i++)inputs[i].value="";document.getElementById("switch-btn").style.display="block";document.getElementById("switch-btn").innerText="";var btn=document.getElementById("btn-submit-text");btn.disabled=false;btn.innerText=""}
function openLogin(){mode="login";resetModal();document.getElementById("modal-title").innerText="Welcome Back";document.getElementById("modal-desc").innerText="Login to continue shopping";document.getElementById("btn-submit-text").innerText="Login";document.getElementById("switch-btn").innerText="Don't have an account? Sign Up";document.getElementById("switch-btn").onclick=openSignup;document.getElementById("modal").style.display="flex"}
function openSignup(){mode="signup";resetModal();document.getElementById("modal-title").innerText="Create Account";document.getElementById("modal-desc").innerText="Join EduMarket today";document.getElementById("username-group").style.display="block";document.getElementById("btn-submit-text").innerText="Sign Up";document.getElementById("switch-btn").innerText="Already have an account? Login";document.getElementById("switch-btn").onclick=openLogin;document.getElementById("modal").style.display="flex"}
function openPayModal(){mode="pay";resetModal();document.getElementById("modal-title").innerText="M-Pesa Payment";document.getElementById("modal-desc").innerText="Enter phone number to pay";document.getElementById("email-group").style.display="none";document.getElementById("password-group").style.display="none";document.getElementById("switch-btn").style.display="none";document.getElementById("mpesa-group").style.display="block";document.getElementById("btn-submit-text").innerText="Pay Now";document.getElementById("modal").style.display="flex"}
function openAddProduct(){if(!localStorage.getItem("user")){showToast("You must be logged in to add products","error");openLogin();return}mode="addProduct";resetModal();document.getElementById("modal-title").innerText="Add New Product";document.getElementById("modal-desc").innerText="Fill in product details";document.getElementById("email-group").style.display="none";document.getElementById("password-group").style.display="none";document.getElementById("switch-btn").style.display="none";document.getElementById("prod-group").style.display="block";document.getElementById("btn-submit-text").innerText="Add Product";document.getElementById("modal").style.display="flex"}
function closeModal(){document.getElementById("modal").style.display="none"}
function submitForm(){var btn=document.getElementById("btn-submit-text");btn.disabled=true;if(mode==="login"){var email=document.getElementById("email").value.trim();var password=document.getElementById("password").value;if(!email||!password){showToast("Fill in all fields","error");btn.disabled=false;return}btn.innerText="Logging in...";fetch(API+"/login",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email:email,password:password})}).then(function(r){return r.json()}).then(function(data){if(data.user){localStorage.setItem("user",JSON.stringify(data.user));showToast("Login successful!","success");closeModal();updateNavbar()}else{showToast(data.message||"Invalid email or password","error");btn.innerText="Login";btn.disabled=false}}).catch(function(){showToast("Could not connect to server","error");btn.innerText="Login";btn.disabled=false})}else if(mode==="signup"){var username=document.getElementById("username").value.trim();var email=document.getElementById("email").value.trim();var password=document.getElementById("password").value;if(!username||!email||!password){showToast("Fill in all fields","error");btn.disabled=false;return}btn.innerText="Creating account...";fetch(API+"/signup",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({username:username,email:email,password:password})}).then(function(r){return{json:r.json(),ok:r.ok}}).then(function(resp){return resp.json.then(function(data){if(resp.ok){showToast("Signup successful! Please login.","success");openLogin()}else{showToast(data.message||"Signup failed","error");btn.innerText="Sign Up";btn.disabled=false}})}).catch(function(){showToast("Could not connect to server","error");btn.innerText="Sign Up";btn.disabled=false})}else if(mode==="addProduct"){var name=document.getElementById("prod-name").value.trim();var price=document.getElementById("prod-price").value;var img=document.getElementById("prod-img").value.trim();if(!name||!price){showToast("Name and Price are required","error");btn.disabled=false;return}if(!img)img="https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&q=80";btn.innerText="Adding...";fetch(API+"/add_product",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({name:name,price:Number(price),img:img})}).then(function(r){return r.json()}).then(function(){showToast("Product added!","success");closeModal();loadProducts()}).catch(function(){showToast("Could not connect to server","error");btn.innerText="Add Product";btn.disabled=false})}else if(mode==="pay"){var phone=document.getElementById("mpesa-phone").value.trim();if(!phone){showToast("Enter phone number","error");btn.disabled=false;return}btn.innerText="Processing...";fetch(API+"/pay",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({phone:phone,product_id:currentProductId})}).then(function(r){return r.json()}).then(function(data){if(data.success){showToast("Check your phone for M-Pesa prompt","success");closeModal()}else{showToast(data.error||"Payment failed","error");btn.innerText="Pay Now";btn.disabled=false}}).catch(function(){showToast("Could not connect to server","error");btn.innerText="Pay Now";btn.disabled=false})}}
function toggleAuthMode(){if(mode==="login")openSignup();else openLogin()}
</script>
</body>
</html>'''


@app.route('/')
def index():
    return Response(HTML_PAGE, mimetype='text/html')


@app.route('/api/health')
def health():
    try:
        db.session.execute(db.text('SELECT 1'))
        product_count = Product.query.count()
        return jsonify({"status": "healthy", "database": "connected", "products": product_count})
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


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
        product = Product(name=data['name'], price=float(data['price']), img=data.get('img', ''))
        db.session.add(product)
        db.session.commit()
        return jsonify(product.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({"message": "All fields are required"}), 400
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"message": "Email already registered"}), 409
        user = User(username=data['username'], email=data['email'], password=data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Signup successful!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({"message": "Email and password required"}), 400
        user = User.query.filter_by(email=data['email'], password=data['password']).first()
        if not user:
            return jsonify({"message": "Invalid email or password"}), 401
        return jsonify({"user": user.to_dict()})
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/pay', methods=['POST'])
def pay():
    try:
        data = request.get_json()
        phone = data.get('phone', '')
        product_id = data.get('product_id')
        if not phone or len(phone) < 10:
            return jsonify({"success": False, "error": "Enter a valid phone number"})
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"success": False, "error": "Product not found"})
        return jsonify({"success": True, "message": "M-Pesa prompt sent to " + phone + " for " + product.name + " (KES " + str(product.price) + ")"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


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
            db.session.add(Product(name=s["name"], price=s["price"], img=s["img"]))
        db.session.commit()
        print("Seeded 8 sample products.")


with app.app_context():
    db.create_all()
    seed_products()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)