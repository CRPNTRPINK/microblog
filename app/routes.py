from flask import render_template, flash, redirect, url_for
from flask import request
from flask_login import current_user, login_user
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse
from app import app
from app.forms import LoginForm, PostForm
from app.models import User, Post, Cinema
from app.forms import RegistrationForm
from app import db
from app import admin
from flask_admin.contrib.sqla import ModelView


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sing In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'Ипполит'},
            'body': 'Какая гадость эта ваша заливная рыба!!'
        }
    ]
    return render_template("index.html", title='Home', posts=posts)

@app.route('/film')
def film():
    films = ['Остаться в живых', 'Убить Билла', 'Джон Уик']
    for film in films:
        if Cinema.query.filter_by(name=film).first() is None:
            post = Cinema(name=film)
            db.session.add(post)
            db.session.commit()
    posts = Cinema.query.all()

    return render_template('film.html', posts=posts)

@app.route('/film/<film_name>')
def film_info(film_name):
    post = Cinema.query.filter_by(name=film_name).first_or_404()
    return render_template('film_info.html', post=post)




class Check(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

admin.add_view(Check(User, db.session))
# admin.add_view(Check(Post, db.session))
admin.add_view(Check(Cinema, db.session))