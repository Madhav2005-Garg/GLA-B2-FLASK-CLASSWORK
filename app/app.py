from flask import Flask, render_template, redirect, url_for, request, session
try:
    from app.model.users import Users, db
    from app.form import RegisterForm, LoginForm
except ImportError:
    from model.users import Users, db
    from form import RegisterForm, LoginForm
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
db_url = os.getenv("DATABASE_URL", "")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+psycopg://", 1)
elif db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)

# Create tables within app context
try:
    with app.app_context():
        db.create_all()
except Exception as e:
    print(f"Database initialization error: {e}")


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("register"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if username already exists
        existing_user = Users.query.filter_by(username=form.username.data).first()
        if existing_user:
            form.username.errors.append("Username already exists")
            return render_template("register.html", form=form)
        
        # Check if email already exists
        existing_email = Users.query.filter_by(email=form.email.data).first()
        if existing_email:
            form.email.errors.append("Email already registered")
            return render_template("register.html", form=form)
        
        try:
            user = Users(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login", success="Registration successful!"))
        except Exception as e:
            db.session.rollback()
            form.email.errors.append("Registration failed. Please try again.")
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    form = LoginForm()
    message = request.args.get("success")
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("dashboard"))
        message = "Invalid username or password"
    return render_template("login.html", form=form, message=message)


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = Users.query.get(session["user_id"])
    if not user:
        session.clear()
        return redirect(url_for("login"))
    message = request.args.get("message")
    message_type = request.args.get("message_type", "success")
    return render_template(
        "dashboard.html",
        username=user.username,
        current_email=user.email,
        message=message,
        message_type=message_type
    )


@app.route("/update-email", methods=["POST"])
def update_email():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    new_email = request.form.get("new_email")
    if not new_email:
        return redirect(url_for("dashboard", message="Email is required", message_type="error"))
    
    # Check if email already exists
    existing_user = Users.query.filter_by(email=new_email).first()
    if existing_user and existing_user.id != session["user_id"]:
        return redirect(url_for("dashboard", message="Email already exists", message_type="error"))
    
    try:
        user = Users.query.get(session["user_id"])
        user.email = new_email
        db.session.commit()
        return redirect(url_for("dashboard", message="Email updated successfully!", message_type="success"))
    except Exception as e:
        db.session.rollback()
        return redirect(url_for("dashboard", message="Failed to update email", message_type="error"))


@app.route("/fetch-users")
def fetch_users():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    users = Users.query.all()
    user = Users.query.get(session["user_id"])
    return render_template(
        "dashboard.html",
        username=user.username,
        current_email=user.email,
        users=users,
        message="Users fetched successfully!",
        message_type="success"
    )


@app.route("/delete-account", methods=["POST"])
def delete_account():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    try:
        user = Users.query.get(session["user_id"])
        if user:
            db.session.delete(user)
            db.session.commit()
        session.clear()
        return redirect(url_for("login", success="Account deleted successfully"))
    except Exception as e:
        db.session.rollback()
        return redirect(url_for("dashboard", message="Failed to delete account", message_type="error"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login", success="Logged out successfully"))


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_ENV") == "production")
