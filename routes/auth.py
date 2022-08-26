from flask import Blueprint,request,redirect,render_template,url_for,session,g,flash
from ..extensions import db
from ..models.users import User
from werkzeug.security import generate_password_hash,check_password_hash
import functools

main = Blueprint('main', __name__)


@main.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


# login required
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('main.login'))

        return view(**kwargs)

    return wrapped_view


# register user
@main.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None

        hashed_password = generate_password_hash(password, method='sha256')

        new_user = User(email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            error = f'User {email} registered. Now Login!'
            flash(error)
            return redirect(url_for('main.login'))
        except:
            error = f'Email {email} has already been taken!'
        
        flash(error)

    return render_template('auth/register.html')

# login user
@main.route('/', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
    
        user = User.query.filter_by(email = email).first()

        if not user or not check_password_hash(user.password, password):
            error = 'Invalid username or password!'
        
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('management.index'))

        flash(error)

    return render_template('auth/login.html')

# logout user
@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))