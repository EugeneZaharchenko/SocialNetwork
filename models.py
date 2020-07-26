from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    posts = db.relationship('Post', foreign_keys='Post.author_id', backref='author', lazy='dynamic')
    activity = db.relationship("Activity", uselist=False, backref="user")

    liked = db.relationship(
        'PostLike',
        foreign_keys='PostLike.user_id',
        backref='user', lazy='dynamic')

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.id).count() > 0

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

    creation = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    login = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    latest_activity = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def latest_login(self):
        login = Activity.query.filter_by(
            id=self.id).update({'login': datetime.utcnow()})
        db.session.commit()

    def latest_usage(self):
        activity = Activity.query.filter_by(
            id=self.id).update({'latest_activity': datetime.utcnow()})
        db.session.commit()


class PostLike(db.Model):
    __tablename__ = 'post_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')

    def __repr__(self):
        return '<Post id {0} containing {1}>'.format(self.id, self.body)
