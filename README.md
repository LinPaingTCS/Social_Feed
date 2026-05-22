# Social Feed Platform

A Flask-based social media application with user authentication, posts, 
comments, and likes.

## Features
- User registration and authentication
- Create and delete posts
- Comment on posts
- Like posts
- User profiles
- Secure password hashing

## Tech Stack
- Backend: Python, Flask
- Database: SQLite with SQLAlchemy ORM
- Frontend: HTML, CSS (Jinja2 templates)
- Security: Werkzeug password hashing

## Installation

```bash
git clone https://github.com/LinPaingTCS/Social_Feed.git
cd Social_Feed
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000`

## Database Schema
- Users (id, username, email, password_hash, bio)
- Posts (id, content, user_id, created_at)
- Comments (id, content, user_id, post_id)
- Likes (id, user_id, post_id)

## Screenshots
[Add 2-3 screenshots here]
