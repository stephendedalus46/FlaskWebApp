from flask import render_template  # function for returning HTML in the function
from flask import url_for  # if there is a change in the root URL then you have to change it in every page where the link is present
from flask import flash  # popup message
from flask import redirect  # function for redirection to another rout
from flask import request  # to access requests from urls
from flask import Blueprint  # to indispose to update not user's post

from flask_login import login_user  # to handle login route
from flask_login import current_user  # to disable possibility to go to login/register route when user is logged in
from flask_login import logout_user  # to handle logout route
from flask_login import login_required  # to disable access to account route while logout

from flaskblog import db, bcrypt  # variables(instances of classes) from __init__

from flaskblog.models import User, Post

from flaskblog.users.forms import RegistrationForm  # class defined by me
from flaskblog.users.forms import LoginForm  # class defined by me
from flaskblog.users.forms import UpdateAccountForm  # class defined by me
from flaskblog.users.forms import RequestResetForm  # class defined by me
from flaskblog.users.forms import ResetPasswordForm  # class defined by me

from flaskblog.users.utils import save_picture
from flaskblog.users.utils import send_reset_email


users = Blueprint('users', __name__)  # similar to creating flask object, users is name of blueprint


@users.route('/register', methods=['GET', 'POST'])  # add methods that this rout can handle with
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')  # flash takes second argument, it might be 1of3 bootsrap classess: success, warning, error
        return redirect(url_for('users.login'))  # login is name of function!
    return render_template('register.html', title='Register', form=form)  # IMPORTANT form=form!!!!


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')  # will go back to route that user was trying to access before login
            return redirect(next_page) if next_page else redirect(url_for('main.home'))  # will go back to route that user was trying to access before login
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='About', form=form)  # IMPORTANT form=form!!!!


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required  # we need to tell this extension where the login route is located (__init__ file)
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('users.account'))  # to avoid post get redirect pattern
    elif request.method == 'GET':  # to avoid post get redirect pattern
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)  # default page = 1
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)  # we don't want to have all() on one page, order_by -> newest on top
    return render_template('user_posts.html', posts=posts, user=user)  # passing also list from code


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')  # flash takes second argument, it might be 1of3 bootsrap classess: success, warning, error
        return redirect(url_for('users.login'))  # login is name of function!
    return render_template('reset_token.html', title='Reset Password', form=form)

