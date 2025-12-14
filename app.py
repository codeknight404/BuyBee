from flask import Flask, render_template, session, redirect, url_for
from config import Config
from db import get_db_connection
from routes.product_routes import product_bp
from routes.auth_routes import auth_bp

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

# Register blueprints
app.register_blueprint(product_bp, url_prefix="/products")
app.register_blueprint(auth_bp, url_prefix="/auth")

@app.route('/')
def home():
    user = session.get('user_name')
    return render_template('index.html', user=user)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT SUM(quantity) AS total_items FROM cart_items WHERE user_id = %s", (user_id,))
    result = cur.fetchone()
    cart_count = result['total_items'] if result['total_items'] else 0
    cur.close()
    conn.close()

    return render_template(
        'dashboard.html',
        user=session.get('user_name'),
        cart_items=cart_count
    )


if __name__ == '__main__':
    app.run(debug=True)
