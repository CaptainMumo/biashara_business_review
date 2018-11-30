from flask import render_template, redirect, request, flash, url_for
from flaskapp import app, bcrypt, db
from flaskapp.forms import SigninForm, SignupForm, RegisterBusinessForm
from flaskapp.models import User, Business, Review
from flask_login import login_user, current_user, logout_user, login_required

"""users = [
        {
            'email':"kamau@gmail.com",
            'password' : "password"
        },
        {
            'email' : "frere@gmail.com"
        }
]"""

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/auth/signup", methods=['GET','POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        """user = {
                'username' : request.form['username'],
                'email' : request.form['email'],
                'location' : request.form['location'],
                'password' : request.form['password']
            }
        users.append(user)"""
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data.lower(), email=form.email.data.lower(),
                    location=form.location.data.lower(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!',category="message")
        return redirect(url_for('signin')) 
        
    return render_template('signup.html', title='Sign Up', form=form) 

@app.route("/auth/signin", methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        #if form.email.data == "frere@gmail.com":#(user['email'] for user in users) and form.password.data == (user['password'] for user in users):
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!',category="message")
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!',category="error")
        
    return render_template('signin.html', title='Sign In', form=form)

@app.route("/auth/signout")
def signout():
    if current_user.is_authenticated:
        logout_user()
        flash('Logged out successfully!',category="message")
        return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route("/businesses/", methods=['GET','POST'])
@login_required
def register_business():
    form = RegisterBusinessForm()
    if form.validate_on_submit():
        business = Business(business_name=form.business_name.data, category=form.category.data, 
                            description=form.description.data, location=form.location.data,
                            email=form.email.data, phone=form.phone.data, owner=current_user)

        db.session.add(business)
        db.session.commit()
        flash("You have successfully registered a business", "message")
        return redirect(url_for('home'))
    return render_template("register_business.html", title="Register Business", form=form)