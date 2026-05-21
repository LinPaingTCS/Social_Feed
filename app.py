from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User, Post, Comment, Like
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///socialfeed.db'
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
db.init_app(app)

with app.app_context():
    db.create_all()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You must be logged in', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('feed'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Log in now.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('feed'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/feed')
@login_required
def feed():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    current_user_id = session.get('user_id')
    return render_template('feed.html', posts=posts, current_user_id=current_user_id)

@app.route('/create_post', methods=['POST'])
@login_required
def create_post():
    content = request.form.get('content')
    user_id = session.get('user_id')
    
    if not content or not content.strip():
        flash('Post cannot be empty', 'error')
        return redirect(url_for('feed'))
    
    post = Post(content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    
    flash('Post created!', 'success')
    return redirect(url_for('feed'))

@app.route('/delete/<int:post_id>', methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    
    if not post:
        flash('Post not found', 'error')
        return redirect(url_for('feed'))
    
    if post.user_id != session.get('user_id'):
        flash('You can only delete your own posts', 'error')
        return redirect(url_for('feed'))
    
    db.session.delete(post)
    db.session.commit()
    
    flash('Post deleted!', 'success')
    return redirect(url_for('feed'))

@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('feed'))
    
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.created_at.desc()).all()
    return render_template('profile.html', user=user, posts=posts)

@app.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get(post_id)
    user_id = session.get('user_id')
    
    if not post:
        flash('Post not found', 'error')
        return redirect(url_for('feed'))
    
    existing_like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
    
    if existing_like:
        db.session.delete(existing_like)
        flash('Like removed', 'success')
    else:
        like = Like(user_id=user_id, post_id=post_id)
        db.session.add(like)
        flash('Post liked!', 'success')
    
    db.session.commit()
    return redirect(url_for('feed'))

if __name__ == '__main__':
    app.run(debug=True)