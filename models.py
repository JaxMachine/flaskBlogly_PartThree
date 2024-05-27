from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

DEFAULT_AVATAR_URL = "https://fastly.picsum.photos/id/374/200/200.jpg?hmac=ifUjaLhaxfMlsBL7zHVuQ1YgZ1ECmNDNG8v0D9uHdIc"


"""Models for Blogly."""

class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(20), nullable=True)
    last_name = db.Column(db.String(20), nullable=True)
    user_email = db.Column(db.String(50), nullable = False, unique=True)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_AVATAR_URL)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def get_full_name(self):
        """Return users' full name"""
        first = ""
        last = ""
        if(self.first_name == ""):
            first = "Unknown"
        else:
            first = self.first_name
        if(self.last_name==""):
            last = "Unknown"
        else:
            last = self.last_name

        return f"{first} {last}"
    



class Post(db.Model):
    """Post Class"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False, unique = False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def date_return(self):
        """Returns in a readable format"""

        return self.created_at.strftime("%a % b %-d %Y, %-I:%M %p")
    

class PostTage(db.Model):
    """Post Tag Model"""

    __tablename__ ='posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    """Tag Class"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, Nullable=False, unique=True)

    posts = db.relationship('Post', secondary='post_tags', cascade="all,delete", backref="tags",)




def connect_db(app):
    """connect to the database"""
    
    db.app = app
    db.init_app(app)