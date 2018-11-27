from flask import Flask, render_template, url_for, redirect, flash, request, jsonify
from forms import SignupForm, SigninForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e8f836430f6c0c054ffe0231a7158fe1'

users = []

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
        return redirect(url_for('home'))
    return render_template('signin.html', title='Sign In', form=form)

if __name__=="__main__":
    app.run(debug=True)

