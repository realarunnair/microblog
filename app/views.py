from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from forms import LoginForm
from models import User, ROLE_USER, ROLE_ADMIN

@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
@login_required
def index():
     user = g.user
     posts = [ # fake array of posts
         { 
           'author': { 'nickname': 'John' }, 
           'body': 'Beautiful day in Portland!' 
         },
         {
           'author': { 'nickname': 'Susan' },
           'body': 'The Avengers movie was so cool!' 
         }
     ]
     return render_template("index.html",
         title = 'Home', user = user,
         posts = posts)
   
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():  #goes to /index if form input is validated.
            session['remember_me'] = form.remember_me.data
            # return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
            uName = form.username.data
            user = User.query.filter_by(nickname = uName).first()
            if user is None:
                flash('Invalid login. Please try again')
                return redirect(url_for('login'))
            remember_me = False
            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)
            login_user(user,remember = remember_me)
            return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', 
        title = 'Sign In',
        form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@lm.user_loader  #function to load user from the database.
def load_user(id):
    return User.query.get(int(id))