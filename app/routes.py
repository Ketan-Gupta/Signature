import os, string, random
from flask import render_template, flash, redirect, url_for, request, jsonify, Response
from app import app, db
from app.forms import LoginForm, RegistrationForm, UploadForm, VirtualIDForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Information, VirtualID
from werkzeug.urls import url_parse
from app.forms import ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_email, send_password_reset_email
from config import basedir
import requests
import json

wrong=[]

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


@app.route('/documents/<username>')
@login_required
def documents(username):
    tempuser=username
    return render_template("document_list.html", username=tempuser)


@app.route('/aadhar')
@login_required
def aadhar():
    username=current_user.username
    image_name="aadhar.jpg"
    document="aadhar"
    display_name="/".join(["images", username, "aadhar.jpg"])
    target = os.path.join(os.path.sep, basedir, 'app', 'static', 'images', username, "aadhar.jpg")
    if not os.path.isfile(target):
        return redirect(url_for('upload', document=document))
    else:
        return redirect(url_for('display', document=document))

    
@app.route('/birth')
@login_required
def birth():
    username=current_user.username
    image_name="birth.jpg"
    document="birth"
    display_name="/".join(["images", username, "birth.jpg"])
    target = os.path.join(os.path.sep, basedir, 'app', 'static', 'images', username, "birth.jpg")
    if not os.path.isfile(target):
        return redirect(url_for('upload', document=document))
    else:
        return redirect(url_for('display', document=document))



@app.route('/domicile')
@login_required
def domicile():
    username=current_user.username
    image_name="domicile.jpg"
    document="domicile"
    display_name="/".join(["images", username, "domicile.jpg"])
    target = os.path.join(os.path.sep, basedir, 'app', 'static', 'images', username, "domicile.jpg")
    if not os.path.isfile(target):
        return redirect(url_for('upload', document=document))
    else:
        return redirect(url_for('display', document=document))



@app.route('/tenth')
@login_required
def tenth():
    username=current_user.username
    image_name="tenth.jpg"
    document="tenth"
    display_name="/".join(["images", username, "tenth.jpg"])
    target = os.path.join(os.path.sep, basedir, 'app', 'static', 'images', username, "tenth.jpg")
    if not os.path.isfile(target):
        return redirect(url_for('upload', document=document))
    else:
        return redirect(url_for('display', document=document))



@app.route('/twelfth')
@login_required
def twelfth():
    username=current_user.username
    image_name="twelfth.jpg"
    document="twelfth"
    display_name="/".join(["images", username, "twelfth.jpg"])
    target = os.path.join(os.path.sep, basedir, 'app', 'static', 'images', username, "twelfth.jpg")
    if not os.path.isfile(target):
        return redirect(url_for('upload', document=document))
    else:
        return redirect(url_for('display', document=document))


@app.route('/upload/<document>', methods=['POST', 'GET'])
@login_required
def upload(document):
    import string
    username=current_user.username
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename=".".join([document, "jpg"])

        target = os.path.join(os.path.sep, basedir, 'app','static', 'images', username)
        if not os.path.isdir(target.encode('ascii', 'ignore')):
            os.mkdir(target)
            
        f.save(target+"/"+filename)
        return redirect(url_for('documents', username=username))
    return render_template('upload.html', form=form, document=document)



@app.route('/display/<document>', methods=["POST", "GET"])
@login_required
def display(document):
    import string
    username=current_user.username
    image_name=document + ".jpg"
    path_name = "/".join(["images", username, image_name])
    return render_template('display.html', username=username, document=document, path_name=path_name)


@app.route('/generatevirtualid/<username>', methods=["POST", "GET"])
@login_required
def generatevirtualid(username):
    form = VirtualIDForm()
    if form.validate_on_submit():
        return redirect(url_for('virtualid', username=username))
    return render_template('generate_virtual_id.html', username=username, form=form)



@app.route('/virtualid/<username>', methods=["POST", "GET"])
@login_required
def virtualid(username):
    user=User.query.filter_by(username=username).first()
    tempid=user.id
    virtualid= VirtualID.query.filter_by(user_id=tempid).first()
    if virtualid is not None:
        retreived_id=virtualid.virtual_id
        passing_id = retreived_id
    else:
        generated_virtual_id=random.randrange(1000000000, 9999999999)
        create_id = VirtualID(user_id=tempid, virtual_id=generated_virtual_id)
        db.session.add(create_id)
        db.session.commit()
        passing_id=generated_virtual_id

    return render_template('display_virtual_id.html', username=username, virtual_id=passing_id)



@app.route('/verification', methods=["GET","POST"])
def verification():
    for i in range(len(wrong)):
        wrong.remove(wrong[i])

    data = request.get_json(force=True)
    if not data['virtualid']:
        return "Error"
    tempid= data['virtualid']
    u = VirtualID.query.filter_by(virtual_id=tempid).first()
    if u is None:
        return "Error"
    userid= u.user_id
    user = Information.query.filter_by(user_id=userid).first()
    print(user.name.encode('ascii','ignore'), user.phone, data['dob'])

    if data['name'] != user.name.encode('ascii','ignore'):
        wrong.append("Name")

    if data['surname'] != user.surname.encode('ascii','ignore'):
        wrong.append("Surname")

    if data['dob'].encode('ascii','ignore') != str(user.dob.date()):
        wrong.append("Date of Birth")

    if data['number'] != user.phone:
        wrong.append("Contact Number")

    if data['tenth'] is not user.tenth:
        wrong.append("Tenth")

    if data['twelfth'] is not user.twelfth:
        wrong.append("Twelfth")

    if data['university'] is not user.university:
        wrong.append("University CGPA")

    if data['domicile'] != user.domicile.encode('ascii','ignore'):
        wrong.append("Domicile")

    return "Verification Processes"

@app.route('/response', methods=["GET"])
def reponse():
    response=wrong
    return jsonify(response)









  








            








    



    




    
















































        





    
    

