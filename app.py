"""Blogly application."""

from flask import Flask, redirect, request, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
debug = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()


@app.route("/")
def home_page():
    """Home page, showing recent posts"""
    
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    return render_template("homepage.html",posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    """404 Page"""

    return render_template('404.html'), 404


##Users

@app.route("/users")
def user_list():
    """list all saved users"""
    users = User.query.all()

    return render_template ("user_list.html", users=users)

@app.route("/users/new")
def new_user():
    """Display Add User Form"""
    title = "Add New User"
    button = "Add User"

    return render_template("user_form.html", title=title, button=button)

@app.route("/users/new", methods=["POST"])
def add_user():
    """Add User to database"""
    user_name = request.form['user_name']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    user_email = request.form['user_email']
    image_url = request.form['image_url']

    user = User(user_name=user_name, first_name=first_name, last_name=last_name,user_email=user_email, image_url=image_url)

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/user/<int:user_id>")
def show_user_details(user_id):
    """Display User Details"""

    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", user=user)

@app.route("/user/<int:user_id>/edit")
def edit_user_form(user_id):
    """Edit user details"""
    user = User.query.get_or_404(user_id)
    title = f"Edit {user.user_name}"
    button="Submit Edits"

    return render_template ("user_form.html", title=title, button=button)


@app.route("/user/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Edit User Details"""

    user = User.query.get_or_404(user_id)
    user.user_name = request.form['user_name']
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.user_email = request.form['user_email']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()


    return redirect("/users")

@app.route("/user/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """remove user from database"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


##Posts

@app.route('/user/<int:user_id>/posts/new')
def new_post_form(user_id):
    """Add a post based on the user_id"""

    user = User.query.get_or_404(user_id)
    return render_template('new_post.html', user=user)

@app.route('/user/<int:user_id>/posts/new', methods=["POST"])
def create_post(user_id):
    """Submit Form for new post creation"""

    user= User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],user=user)
    
    db.session.add(new_post)
    db.session.commit()
    flash(f"Submitted '{new_post.title}'" )

    return redirect(f"/user/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post_details(post_id):
    """Page with information for a specific post"""

    post = Post.query.get_or_404(post_id)
    return render_template("post_info.html", post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post_page(post_id):
    """Page for editing Post information"""

    post= Post.query.get_or_404(post_id)
    return render_template("edit_post.html", post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    """Edit post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Edited {post.title}")

    return redirect(f"/user/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete Post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Deleted {post.title}")

    return redirect(f"/user/{post.user_id}")


#Tags

@app.route('/tags')
def show_all_tags():
    """Page with all tags listed"""

    tags = Tag.query.all()
    return render_template("tag_index.html", tags=tags)

@app.route('/tags/new')
def new_tag():
    """Form for adding new tag"""

    posts = Post.query.all()
    return render_template("new_tag.html", posts=posts)

@app.route("/tags/new", methods=["POST"])
def add_new_tag():
    """Logic to handle adding a new tag"""

    post_ids=[int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"New Tag {new_tag}")

    return redirect("/tags")

@app.route('/tags/<int:tag:tag_id>')
def tag_details(tag_id):
    """Tag Details page"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_details.html', tag=tag)

@app.route("/tags/<int:tag_id>/edit")
def edit_a_tag(tag_id):
    """Edit an existing tag form"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('edit_tag.html', tag=tag, posts=posts)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Submit tag edits"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids=[int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    flash(f"{tag.name} has been edited")
    return redirect("/tags")

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Delete Specified Tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"{tag.name} deleted")

    return redirect("/tags")