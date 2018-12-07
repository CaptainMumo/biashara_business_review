from flask import render_template, redirect, request, flash, url_for
from flaskapp import app, bcrypt, db
from flaskapp.forms import SigninForm, SignupForm, BusinessForm, BusinessReviewForm, SearchForm
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

@app.route("/businesses/register", methods=['GET','POST'])
@login_required
def register_business():
    form = BusinessForm()
    if form.validate_on_submit():
        business = Business(business_name=form.business_name.data, category=form.category.data, 
                            description=form.description.data, location=form.location.data,
                            email=form.email.data, phone=form.phone.data, owner=current_user)

        db.session.add(business)
        db.session.commit()
        flash("You have successfully registered a business", "message")
        return redirect(url_for('home'))
    return render_template("register_business.html", title="Register Business", form=form, legend='Register Business')

@app.route("/businesses", methods=['GET','POST'])
def view_businesses():
    businesses=Business.query.all()
    return render_template("view_businesses.html", title="View Businesses", businesses=businesses)

@app.route("/businesses/<business_id>", methods=['GET','POST'])
def view_business(business_id):
    business = Business.query.get_or_404(business_id)
    return render_template('view_business.html', title='View Business', business=business)

@app.route("/businesses/<int:business_id>/update", methods=['GET','POST','PUT'])
@login_required
def update_business(business_id):
    business = Business.query.get_or_404(business_id)
    if business.owner != current_user:
        abort(403)
    form = BusinessForm()
    if form.validate_on_submit():
        business.business_name = form.business_name.data
        business.category = form.category.data
        business.description = form.description.data
        business.location = form.location.data
        business.email = form.email.data
        business.phone = form.phone.data
        db.session.commit()
        flash('Business profile has been updated!','message')
        return redirect(url_for('view_business', business_id=business.id))
    elif request.method == 'GET':
        form.business_name.data = business.business_name
        form.category.data = business.category
        form.description.data = business.description
        form.location.data = business.location
        form.email.data = business.email
        form.phone.data = business.phone
    return render_template('register_business.html', title='Update Business', form=form, legend='Update Business')

@app.route("/businesses/<business_id>/delete", methods=['POST'])
@login_required
def delete_business(business_id):
    business = Business.query.get_or_404(business_id)
    if business.owner != current_user:
        abort(403)
    db.session.delete(business)
    db.session.commit()
    flash('The business has been removed successfully!','message')
    return redirect(url_for('view_businesses'))

@app.route("/businesses/<business_id>/postreview", methods=['GET','POST'])
@login_required
def post_review(business_id):
    business = Business.query.get_or_404(business_id)
    form = BusinessReviewForm()
    if form.validate_on_submit():
        review = Review(title=form.title.data, content=form.content.data, author=current_user, business=business)
        db.session.add(review)
        db.session.commit()
        flash("Your review has been posted!", "message")
        return redirect(url_for('view_business', business_id=business.id))
    return render_template('review.html', title='Post Review', form=form)

@app.route("/businesses/<business_id>/reviews", methods=['GET'])
def view_reviews(business_id):
    reviews = Review.query.all()
    business = Business.query.get_or_404(business_id)
    return render_template('view_business.html', title="View Reviews", reviews=reviews, business=business)

@app.route("/businesses/search", methods=['GET'])
def search():
    businesses = Business.query.whoosh_search(request.args.get('category')).all()
    return render_template('view_businesses.html', title="View businesses", businesses=businesses)
