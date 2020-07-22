import datetime
import uuid
from functools import wraps

import jwt
from flask import jsonify, request, make_response, Response, session, abort
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from models import User, Post


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/')
def home():
    status_code = Response(status=201)
    return status_code


@app.route('/signup', methods=['POST'])
# @token_required
def create_user():
    data = request.get_json()

    name = data['name']
    email = data['email']
    password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), username=name, email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})


@app.route('/login')
def login():
    auth = request.authorization
    print(str(auth))

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('No such user', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})


@app.route('/logout')
# @is_logged_in
def logout():
    session.clear()
    # flash('You are now logged out', 'success')
    # return redirect(url_for('login'))


@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.username
    user_data['password'] = user.password

    return jsonify({'user' : user_data})


@app.route('/user/<string:username>/add_post', methods=['POST'])
@token_required
def add_post(current_user, username):
    data = request.get_json()

    body = data['body']
    user = User.query.filter_by(username=username).first()
    user_id = user.id

    new_post = Post(body=body, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    return jsonify({'message': 'New post of user {} created!'.format(username)})


@app.route('/like/<int:post_id>/<int:user_id>')
# @login_required
def like(post_id,user_id):
    posts = Post.select().where(Post.id == post_id)
    if posts.count() == 0:
        abort(404)

    post = Post.select().where(Post.id == post_id).get()


@app.route('/dislike/<int:post_id>/<int:user_id>')
# @login_required
def dislike(post_id,user_id):
    posts = Post.select().where(Post.id == post_id)

    if posts.count() == 0:
        abort(404)

    post = Post.select().where(Post.id == post_id).get()