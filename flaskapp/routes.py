from flask import render_template, redirect, request, flash, url_for
from flaskapp import app
from flaskapp.forms import SigninForm, SignupForm


users = [
        {
            'email':"kamau@gmail.com",
            'password' : "password"
        },
        {
            'email' : "frere@gmail.com"
        }
]

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/auth/signup", methods=['GET','POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():

        user = {
                'username' : request.form['username'],
                'email' : request.form['email'],
                'location' : request.form['location'],
                'password' : request.form['password']
            }
        
        users.append(user)
        flash('Account created successfully!',category="message")
        return redirect(url_for('signin')) 
        
    return render_template('signup.html', title='Sign Up', form=form, users=users) 

@app.route("/auth/signin", methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        
        if form.email.data == "frere@gmail.com":#(user['email'] for user in users) and form.password.data == (user['password'] for user in users):
            flash('Logged in successfully!',category="message")
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!',category="error")
        
    return render_template('signin.html', title='Sign In', form=form)