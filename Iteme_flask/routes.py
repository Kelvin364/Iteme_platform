from flask import flash, redirect, render_template, request, url_for, Blueprint
from app import Student, app, db
from werkzeug.security import generate_password_hash, check_password_hash
# from db_methods import add_student
from flask_login import LoginManager, login_user, current_user, login_required, logout_user


auth = Blueprint('auth', __name__)
main = Blueprint('main', __name__)


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))

""" route for landing page"""
@main.route('/', strict_slashes=False)
def home():
    return render_template('landing.html')

""" routes for dashboard """
@main.route('/stories', strict_slashes=False)
# @login_required
def dashboard():
    # name = current_user.f_name + ' ' + current_user.l_name  
    return render_template('iteme.html')

# @main.route('/findpeer', strict_slashes=False)
# @login_required
# def find_peer():
#     return render_template('findpeer.html')

# @main.route('/wifi', strict_slashes=False)
# @login_required
# def wifi():
#     return render_template('wifi.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

"""routes for login and sign up"""
@auth.route('/login', strict_slashes=False)
def login():
    return render_template('login.html')

@auth.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login_post():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = True if request.form.get('remember') else False

        if not email or not password:
            flash('All fields are required!', 'Error')
        student = Student.query.filter_by(email=email).first()

        if not student or not check_password_hash(student.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))
        login_user(student, remember=remember)
        return redirect(url_for('main.dashboard')) #changed from dashboard to profile

@auth.route('/register', strict_slashes=False)
def register():
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register_post():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        re_password = request.form['re-password']
        
        # Validate input data
        if not email or not password or not re_password:
            flash("All fields are required.", "error")
            return redirect(url_for('auth.register'))
        # check if the retyped password is the same as the first password
        if password != re_password:
            flash("Password unmatched.", "Error")
            return redirect(url_for('auth.register'))
        # Check if the email and password already exists in the database
        existing_email = Student.query.filter_by(email=email).first()
        if not existing_email:
            flash("Not ALX Student!")
        if existing_email and existing_email.password != None:
            flash("Already Registered. Go to <a href='"+ url_for('auth.login') +"'>Login Page</a>", "error")
            return redirect(url_for('auth.register'))
        else:
            # add user's hashed password to the database
            try:
                existing_email.password = generate_password_hash(password, method='scrypt')
                db.session.add(existing_email)
                db.session.commit()
                flash("User registered successfully!", "success")
                return redirect(url_for('auth.login'))
            except Exception as e:
                flash(f"Error registering user: {str(e)}", "error")
                return redirect(url_for('auth.register'))


app.register_blueprint(auth)
app.register_blueprint(main)