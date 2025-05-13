from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from db import db, Usuario

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        user = Usuario.query.filter_by(correo=email).first()

        if user and check_password_hash(user.contraseña, contraseña):
            login_user(user)
            return redirect(url_for('index'))  # Bien, porque tu función se llama `index`

        else:
            flash('Credenciales inválidas')
    return render_template('login.html')

@auth.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        hashed_pw = generate_password_hash(contraseña)
        nuevo_usuario = Usuario(correo=email, contraseña=hashed_pw)


        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Usuario registrado exitosamente')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

