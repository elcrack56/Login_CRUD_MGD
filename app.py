
import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, flash
from pymongo import MongoClient
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta 

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)
db = client.inventario_db 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login' 
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.' 

from models.user_model import User

@login_manager.user_loader
def load_user(user_id):
    """
    Dado un user_id, esta función debe cargar y retornar el objeto User.
    Flask-Login lo usa para mantener al usuario logueado entre solicitudes.
    """
    return User.get_by_id(user_id, db)

from controllers.auth_controller import auth_bp
from controllers.product_controller import product_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(product_bp, url_prefix='/products')

@app.route('/')
@login_required 
def index():
    return redirect(url_for('product.list_products'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404 

if __name__ == '__main__':
    app.run(debug=True)