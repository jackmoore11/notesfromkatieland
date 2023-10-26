from datetime import timedelta
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from notesfromkatieland import db, bcrypt
from notesfromkatieland.models import User, Post
from notesfromkatieland.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from notesfromkatieland.users.utils import savePicture, sendResetEmail

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.testimonials'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashedPassword)
        db.session.add(user)
        db.session.commit()
        flash('Account created. Please log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.testimonials'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data, duration=timedelta(days=1))
            nextPage = request.args.get('next')
            if nextPage:
                return redirect(nextPage)
            else:
                return redirect(url_for('main.testimonials'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.testimonials'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            imageFilename = savePicture(form.picture.data)
            current_user.imageFile = imageFilename
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account information has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    imageFile = url_for('static', filename=f'profile_pics/{current_user.imageFile}')
    return render_template('account.html', title='Account', imageFile=imageFile, form=form)

@users.route('/user/<string:username>')
@login_required
def userPosts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.datePosted.desc()).paginate(page=page, per_page=5)
    return render_template('userPosts.html', posts=posts, user=user)

@users.route('/resetPassword', methods=['GET', 'POST'])
def resetRequest():
    if current_user.is_authenticated:
        return redirect(url_for('main.testimonials'))
    
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        sendResetEmail(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))

    return render_template('resetRequest.html', title='Reset Password', form=form)

@users.route('/resetPassword/<token>', methods=['GET', 'POST'])
def resetToken(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.testimonials'))
    
    user = User.verifyResetToken(token)
    if user is None:
        flash('That is an invalid or expired token.', 'warning')
        return redirect(url_for('users.resetRequest'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashedPassword
        db.session.commit()
        flash('Password reset was successful. Please log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('resetToken.html', title='Reset Password', form=form)