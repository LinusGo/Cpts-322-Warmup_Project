from __future__ import print_function
from flask_login import current_user, login_user, logout_user, login_required
from flask_wtf import form

from app.forms import LoginForm, EmptyForm

import sys
from datetime import datetime
from pprint import pprint

from flask import render_template, flash, redirect, url_for, request
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import desc

from app import app, db
from app.models import User
from app.forms import PostForm, SortForm, RegistrationForm
from app.models import Post
from app.models import Tag
from app.models import postTags


@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()
    if Tag.query.count() == 0:
        tags = ['funny', 'inspiring', 'true-story', 'heartwarming', 'friendship']
        for t in tags:
            db.session.add(Tag(name=t))
            db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    sortform = SortForm()
    selected = dict(sortform.sort.choices).get(int(request.args.get('sort', 0)))

    values = {
        'Happiness level': 'happiness_level',
        '# of likes': 'likes',
        'Title': 'title',
        'Date': 'timestamp'
    }
    if request.args.get('checkbox') == 'y':
        posts = Post.query.filter(User.id == current_user.get_id()).order_by(
            getattr(Post, values.get(selected, 'title')).desc())
        return render_template('index.html', posts=posts.all(), title="Smile Portal", sortform=sortform)
    else:
        posts = Post.query.order_by(getattr(Post, values.get(selected, 'title')).desc())
        return render_template('index.html', posts=posts.all(), title="Smile Portal", sortform=sortform)


@app.route('/postsmile', methods=['GET', 'POST'])
@login_required
def postSmile():
    form = PostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            post = Post(title=form.title.data,
                        body=form.body.data,
                        happiness_level=form.happiness_level.data,
                        user_id=current_user.get_id()
                        )

            for t in form.tag.data:
                post.tags.append(t)
            db.session.add(post)
            db.session.commit()
            flash('Post was successfully added')
            return redirect('/index')

    return render_template('create.html', title="Post New Smile", form=form)


@app.route('/like/<post_id>', methods=['GET'])
@login_required
def like(post_id):
    pi = Post.query.get(post_id)
    pi.likes += 1
    db.session.add(pi)
    db.session.commit()
    posts = Post.query.order_by(Post.timestamp.desc())
    pc = posts.count()
    # return redirect(url_for('index'))
    return render_template('index.html', title="Smile Portal", posts=posts.all(), smilecount=pc, form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.add(current_user)
        db.session.commit()


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.get_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/delete/<post_id>', methods=['POST', 'DELETE'])
@login_required
def delete(post_id):
    form = EmptyForm()
    if form.validate_on_submit():
        thepost = Post.query.filter_by(id=post_id).first()
        if thepost is None:
            flash('Post with id "{}" not found.'.format(post_id))
            return redirect(url_for('index'))

        for t in thepost.tags:
            thepost.tags.remove(t)
        current_user.delete(thepost)
        db.session.delete(thepost)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
