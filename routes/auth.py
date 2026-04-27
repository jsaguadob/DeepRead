from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models.user import Usuario
import bcrypt

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario.password_hash.encode('utf-8')):
            login_user(usuario)
            flash('¡Bienvenido de nuevo!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Email o contraseña incorrectos.', 'error')
    
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        tipo = request.form.get('tipo', 'gratuito')
        rol = request.form.get('rol', 'estudiante')
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('register.html')
        
        if '.edu' not in email and tipo == 'institucional':
            flash('Cuenta institucional requiere email .edu', 'error')
            return render_template('register.html')
        
        if Usuario.query.filter_by(email=email).first():
            flash('El email ya está registrado.', 'error')
            return render_template('register.html')
        
        if Usuario.query.filter_by(username=username).first():
            flash('El nombre de usuario ya está en uso.', 'error')
            return render_template('register.html')
        
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        if tipo == 'gratuito':
            rol = 'estudiante'
        
        nuevo_usuario = Usuario(
            username=username,
            email=email,
            password_hash=password_hash,
            rol=rol,
            tipo_usuario=tipo
        )
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('¡Cuenta creada! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('main.index'))