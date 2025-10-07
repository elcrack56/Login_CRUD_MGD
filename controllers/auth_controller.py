from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import User
from bson.objectid import ObjectId

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    from app import db
    """
    Ruta para el registro de nuevos usuarios.
    Si el usuario ya está autenticado, lo redirige.
    """
    if current_user.is_authenticated:
        flash('Ya has iniciado sesión.', 'info')
        return redirect(url_for('product.list_products'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Por favor, ingresa un usuario y una contraseña.', 'danger')
            return render_template('auth/register.html', username=username)

        if db.users.find_one({'username': username}):
            flash('El nombre de usuario ya existe. Elige otro.', 'warning')
            return render_template('auth/register.html', username=username)

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        db.users.insert_one({'username': username, 'password': hashed_password})
        
        flash('¡Registro exitoso! Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    from app import db
    """
    Ruta para el inicio de sesión de usuarios existentes.
    Si el usuario ya está autenticado, lo redirige.
    """
    if current_user.is_authenticated:
        flash('Ya has iniciado sesión.', 'info')
        return redirect(url_for('product.list_products'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember_me') == 'on'

        user = User.get_by_username(username, db)

        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            flash(f'¡Bienvenido de nuevo, {username}!', 'success')
            
            next_page = request.args.get('next')
            return redirect(next_page or url_for('product.list_products'))
        else:
            flash('Usuario o contraseña incorrectos. Inténtalo de nuevo.', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """
    Ruta para cerrar la sesión del usuario actual.
    """
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('auth.login'))