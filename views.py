import datetime
import uuid
from functools import wraps

import jwt
from flask import jsonify, request, make_response, Response, session, abort
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from models import User, Post, PostLike, Activity


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/')
def home():
    status_code = Response(status=200)
    return status_code


@app.route('/signup', methods=['POST'])
def create_user():
    data = request.get_json()

    name = data['name']
    email = data['email']
    password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), username=name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    creation = Activity(user_id=new_user.id)
    db.session.add(creation)
    db.session.commit()

    return jsonify({'message': 'New user named {0}, id: {1} was created!'.format(name, new_user.public_id)})


@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()

    latest_login = Activity.query.filter_by(user_id=user.id).first()
    latest_login.latest_login()

    if not user:
        return make_response('No such user', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120)},
            app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@app.route('/users')
@token_required
def get_all_users(current_user):
    users = User.query.order_by(User.username).all()

    if not users:
        return jsonify({'message': 'No users yet!'})

    users_data = {}
    for user in users:
        num = user.id
        id = user.public_id
        users_data[num] = id

    return jsonify(users_data)

@app.route('/user/<public_id>')
@token_required
def get_one_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.username
    user_data['password'] = user.password

    activity = Activity.query.filter_by(user_id=user.id).first()
    user_data['created'] = activity.creation
    user_data['last_login'] = activity.login

    return jsonify({'user': user_data})


@app.route('/user/<string:username>/add_post', methods=['POST'])
@token_required
def add_post(current_user, username):
    data = request.get_json()

    body = data['body']
    user = User.query.filter_by(username=username).first()
    user_id = user.id

    new_post = Post(body=body, author_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    return jsonify({'message': 'New post of user {} created!'.format(username)})


@app.route('/user/<int:user_id>/post/<int:post_id>/action/<string:action>', methods=['POST'])
@token_required
def like_action(current_user, user_id, post_id, action):
    posts = Post.query.filter(Post.id == post_id).all()
    if len(posts) == 0:
        abort(404)
    print(posts)

    post = Post.query.filter_by(id=post_id).first_or_404()

    user = User.query.filter_by(id=user_id).first()

    if action == 'like':
        post.recipient_id = user_id
        user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        post.recipient_id = 0
        user.unlike_post(post)
        db.session.commit()

    return jsonify({'message': 'New {0} of user {1} to post_id {2} created!'.format(action, user_id, post_id)})


@app.route('/analitics/')
def get_analitics():
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")

    start = datetime.datetime.strptime(date_from, format('%Y-%m-%d'))
    end = datetime.datetime.strptime(date_to, format('%Y-%m-%d'))

    likes = PostLike.query.filter(PostLike.timestamp >= start).filter(PostLike.timestamp <= end).all()
    print(len(likes))
    status_code = Response(status=200)
    return status_code