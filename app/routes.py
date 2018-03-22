from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Information
from werkzeug.urls import url_parse
from app.forms import ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_email, send_password_reset_email


@app.route('/')
@app.route('/index')
@login_required
def index():
    user={'username': current_user.username}
    posts=[
            {
                'title':" Database section denotes the user information",
                'information':" Important, User cannot alter the database"
            },
            {
                'title':" Click on \"Generate Virutal ID \" to generate virtual Id",
                'information': " Virutal Id is a token used for user authentication"
            }
        ]

    return render_template('index.html', title="Home", posts=posts)

@ app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('index')
        return redirect(next_page)
    
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Registration Successful')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user= User.query.filter_by(username=username).first_or_404()
    temp_id=user.id
    information= Information.query.filter_by(user_id=temp_id).first_or_404()
    return render_template('user.html', user=current_user.username, information=information)

@app.route('/reset_password_request', methods=["GET","POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
 
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check Email for Password Reset Instructions')

        return redirect(url_for('login'))

    return render_template('reset_password_request.html', title='Password Rest',form=form)
                

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user= User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        #User is already added, No "db.session.add()
        flash('Password Reset Successfully')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)








    
    

