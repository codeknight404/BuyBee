from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        username = request.form.get('name') 
        email = request.form.get('email')
        password = request.form.get('password')
        hashed = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                           (username, email, hashed))
            conn.commit()
            flash("Account created successfully!", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f"Error: {e}", "danger")
        finally:
            cursor.close()
            conn.close()

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
    
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['username']
            session['user_role'] = user.get('role', 'user') 
            
            flash(f"Welcome back, {session['user_name']}!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password", "danger")

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))