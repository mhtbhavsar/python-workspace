from flask import request, render_template, url_for, flash, redirect
from flaskblog.forms import RegistrationForm, LoginForm, PostForm
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flaskblog.models import User, Post
from flaskblog import app, db

login_manager = LoginManager(app)

@login_manager.user_loader
def get_user(user_id):
  return User.query.get(int(user_id))


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=Post.query.order_by(Post.id.desc()).all())

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for(home))
    form = RegistrationForm()
    if form.validate_on_submit():
        print(request.form['username'])
        user = User(username = request.form['username'], email = request.form['email'], password = request.form['password'])
        print(user)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(home))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            flash('Login Successfull.', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login unsuccessfull. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = request.form['title'], content = request.form['content'], user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash(f'Post successfully created', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='Create Post', form=form)

