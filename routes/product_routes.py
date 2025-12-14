from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_db_connection
from functools import wraps
from werkzeug.utils import secure_filename
import os
import json

product_bp = Blueprint("product", __name__)

# Folder for storing uploaded images
UPLOAD_FOLDER = os.path.join(os.getcwd(), "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("user_role") != "admin":
            flash("Admin access only!", "danger")
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)

    return wrapper


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first!", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return wrapper


# Admin Routes
@product_bp.route("/admin", endpoint="admin_dashboard")
@admin_required
def admin_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products ORDER BY id DESC")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("admin_dashboard.html", products=products)


@product_bp.route("/admin/add", methods=["GET", "POST"], endpoint="add_product")
@admin_required
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        stock = request.form["stock"]

        # Handle image upload
        image_file = request.files.get("image")
        image_filename = None
        if image_file and image_file.filename != "":
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(UPLOAD_FOLDER, image_filename))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, description, price, stock, image) VALUES (%s,%s,%s,%s,%s)",
            (name, description, price, stock, image_filename),
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("✅ Product added successfully!", "success")
        return redirect(url_for("product.admin_dashboard"))

    return render_template("add_product.html")


@product_bp.route(
    "/admin/edit/<int:product_id>", methods=["GET", "POST"], endpoint="edit_product"
)
@admin_required
def edit_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id=%s", (product_id,))
    product = cursor.fetchone()

    if not product:
        flash("Product not found!", "danger")
        return redirect(url_for("product.admin_dashboard"))

    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        stock = request.form["stock"]

        image_file = request.files.get("image")
        image_filename = product["image"]  # keep existing
        if image_file and image_file.filename != "":
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(UPLOAD_FOLDER, image_filename))

        cursor.execute(
            "UPDATE products SET name=%s, description=%s, price=%s, stock=%s, image=%s WHERE id=%s",
            (name, description, price, stock, image_filename, product_id),
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("✅ Product updated successfully!", "success")
        return redirect(url_for("product.admin_dashboard"))

    cursor.close()
    conn.close()
    return render_template("edit_product.html", product=product)


@product_bp.route("/admin/delete/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # First remove any cart references for this product
        cursor.execute("DELETE FROM cart_items WHERE product_id = %s", (product_id,))
        conn.commit()

        # Then delete the product itself
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()

        cursor.close()
        conn.close()
        return redirect(url_for("product.list_products"))

    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        print(f"❌ Error deleting product: {e}")
        return "An error occurred while deleting the product.", 500


# User Product Routes
@product_bp.route("/", endpoint="list_products")
def list_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products ORDER BY id DESC")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("products.html", products=products)


# Cart Routes

# Cart Routes


@product_bp.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    if "user_id" not in session:
        flash("Please login to add items to your cart.", "warning")
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    # Ensure quantity is handled safely, defaulting to 1
    try:
        quantity = int(request.form.get("quantity", 1))
    except ValueError:
        flash("Invalid quantity value.", "danger")
        return redirect(url_for("product.list_products"))

    if quantity < 1:
        flash("Quantity must be at least 1.", "warning")
        return redirect(request.referrer or url_for("product.list_products"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if item already in cart
    cursor.execute(
        "SELECT quantity FROM cart_items WHERE user_id=%s AND product_id=%s",
        (user_id, product_id),
    )
    row = cursor.fetchone()

    if row:
        cursor.execute(
            "UPDATE cart_items SET quantity = quantity + %s WHERE user_id=%s AND product_id=%s",
            (quantity, user_id, product_id),
        )
    else:
        cursor.execute(
            "INSERT INTO cart_items (user_id, product_id, quantity) VALUES (%s,%s,%s)",
            (user_id, product_id, quantity),
        )

    conn.commit()
    cursor.close()
    conn.close()

    flash("✅ Item added to cart!", "success")
    # Redirect to the cart view page instead of the product list page for better user flow
    return redirect(url_for("product.view_cart"))


@product_bp.route("/cart/remove/<int:product_id>", methods=["POST"])
@login_required
def remove_from_cart(product_id):
    """
    Remove a product entirely from the user's cart.
    Redirects to view_cart() to render the updated HTML page.
    """
    user_id = session.get("user_id")

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM cart_items WHERE user_id=%s AND product_id=%s",
            (user_id, product_id),
        )
        conn.commit()
        flash("Item successfully removed from cart.", "info")
    except Exception as e:
        print(f"DB Error removing from cart: {e}")
        if conn:
            conn.rollback()
        flash("A database error occurred during item removal.", "danger")
    finally:
        if conn:
            conn.close()

    # **The return statement that triggers the HTML update via full page reload:**
    return redirect(url_for("product.view_cart"))


@product_bp.route("/cart/update/<int:product_id>", methods=["POST"])
def update_cart(product_id):
    """
    Updates the quantity of a product in the cart or removes it if quantity is <= 0.
    Redirects to view_cart() to render the updated HTML page.
    """
    if "user_id" not in session:
        flash("Please login to update your cart.", "warning")
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    try:
        quantity = int(request.form.get("quantity", 1))
    except ValueError:
        flash("Invalid quantity value submitted.", "danger")
        return redirect(url_for("product.view_cart"))

    conn = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if quantity <= 0:
            # If quantity is zero or less, DELETE the item from the cart
            cursor.execute(
                "DELETE FROM cart_items WHERE user_id=%s AND product_id=%s",
                (user_id, product_id),
            )
            conn.commit()
            flash("Item removed from cart.", "info")
        else:
            # Otherwise, UPDATE the quantity
            cursor.execute(
                "UPDATE cart_items SET quantity=%s WHERE user_id=%s AND product_id=%s",
                (quantity, user_id, product_id),
            )
            conn.commit()
            flash("Cart quantity updated successfully!", "success")

    except Exception as e:
        print(f"DB Error updating cart: {e}")
        if conn:
            conn.rollback()
        flash("A database error occurred while updating your cart.", "danger")
    finally:
        if conn:
            conn.close()

    # **The return statement that triggers the HTML update via full page reload:**
    return redirect(url_for("product.view_cart"))


@product_bp.route("/cart")
def view_cart():
    if "user_id" not in session:
        flash("Login required", "warning")
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT p.id, p.name, p.price, p.image, c.quantity
        FROM cart_items c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id=%s
    """,
        (user_id,),
    )
    cart_items = cursor.fetchall()

    total = sum(item["price"] * item["quantity"] for item in cart_items)

    cursor.close()
    conn.close()
    return render_template("cart.html", cart_items=cart_items, cart_total=total)


# Product Reviews (Text File)
@product_bp.route("/product/<int:product_id>/reviews", methods=["GET", "POST"])
def product_reviews(product_id):
    review_file = f"reviews/reviews_{product_id}.txt"
    os.makedirs("reviews", exist_ok=True)

    if request.method == "POST":
        name = request.form["name"]
        rating = int(request.form["rating"])
        comment = request.form["comment"]

        with open(review_file, "a", encoding="utf-8") as f:
            f.write(
                json.dumps({"name": name, "rating": rating, "comment": comment}) + "\n"
            )

        flash("Review submitted!", "success")
        return redirect(url_for("product.product_reviews", product_id=product_id))

    reviews = []
    if os.path.exists(review_file):
        with open(review_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    reviews.append(json.loads(line.strip()))
                except:
                    continue

    return render_template("reviews.html", product_id=product_id, reviews=reviews)
