from __future__ import print_function
import sys
from datetime import datetime
from pprint import pprint

from flask import render_template, flash, redirect, url_for, request
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import desc

from app import app, db

from app.forms import PostForm, SortForm
from app.models import Post
from app.models import Tag
from app.models import postTags


@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()
    # p = Post(title="Smile test post - 1",
    #          body="First smile post.Maximum 1500 characters. Don't forget to smile today!",
    #          likes=5)
    # db.session.add(p)
    # db.session.commit()
    # print(str(Post.query.limit(1).all()[0]))
    if Tag.query.count() == 0:
        tags = ['funny', 'inspiring', 'true-story', 'heartwarming', 'friendship']
        for t in tags:
            db.session.add(Tag(name=t))
            db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    sortform = SortForm()
    selected = dict(sortform.sort.choices).get(int(request.args.get('sort', 0)))

    values = {
        'Happiness level': 'happiness_level',
        '# of likes': 'likes',
        'Title': 'title',
        'Date': 'timestamp'
    }
    posts = Post.query.order_by(getattr(Post, values.get(selected, 'title')).desc())
    return render_template('index.html', posts=posts.all(), sortform=sortform)


@app.route('/postsmile', methods=['GET', 'POST'])
def postSmile():
    form = PostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            post = Post(title=request.form['title'],
                        body=request.form['body'],
                        happiness_level=int(request.form['happiness_level'])
                        )
            for t in form.tag.data:
                post.tags.append(t)
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
    # return redirect(url_for('index'))
    return render_template('index.html', title="Smile Portal", posts=posts.all(), smilecount=pc)
