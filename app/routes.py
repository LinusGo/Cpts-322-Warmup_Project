from __future__ import print_function
import sys
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_sqlalchemy import sqlalchemy

from app import app, db

from app.forms import PostForm
from app.models import Post


@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()
    p = Post(title="Smile test post - 1",
             body="First smile post.Maximum 1500 characters. Don't forget to smile today!",
             likes=5)
    db.session.add(p)
    db.session.commit()
    print(str(Post.query.limit(1).all()[0]))
    # if Tag.query.count() == 0:
    #     tags = ['funny','inspiring', 'true-story', 'heartwarming', 'friendship']
    #     for t in tags:
    #         db.session.add(Tag(name=t))
    #     db.session.commit()


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template('index.html', title="Smile Portal", posts=posts.all())


@app.route('/postsmile', methods=['GET', 'POST'])
def postSmile():
    form = PostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            post = Post(title=request.form['title'],
                        body=request.form['body'],
                        happiness_level=int(request.form['happiness_level'])
                        )
            db.session.add(post)
            db.session.commit()
            flash('Post was successfully added')
            return redirect('/index')

    return render_template('create.html', title="Post New Smile", form=form)


@app.route('/like/<post_id>', methods=['GET'])
def like(post_id):
    pi = Post.query.get(post_id)
    pi.likes += 1
    db.session.add(pi)
    db.session.commit()
    posts = Post.query.order_by(Post.timestamp.desc())
    pc = posts.count()
    return render_template('index.html', title="Smile Portal", posts=posts.all(),smilecount = pc )
