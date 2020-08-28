from __future__ import print_function
import sys
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_sqlalchemy import sqlalchemy

from app import app,db

from app.forms import PostForm
from app.models import Post


@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()
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


