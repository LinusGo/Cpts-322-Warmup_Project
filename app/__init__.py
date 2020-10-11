import flask_login
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
moment = Moment(app)


from app import routes, models, errors

db.create_all()

if __name__ == '__main__':
    p = models.Post(title="Smile test post - 1",
                    body="First smile post.Maximum 1500 characters. Don't forget to smile today!",
                    likes=5)
    db.session.add(p)
    db.session.commit()
    print(str(models.Post.query.limit(1).all()[0]))
