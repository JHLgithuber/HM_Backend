from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies, create_refresh_token)

app = Flask(__name__)
socketio = SocketIO(app)

logs = []  # 로그를 저장할 리스트

@app.route('/')
def index():
    app.logger.info('인덱스 페이지에 접근됨')
    return render_template('index.html')

@app.route('/logs')
def show_logs():
    return "LOG:\n"+jsonify(logs)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = "Config.key"
#app.config['JWT_ACCESS_TOKEN_EXPIRES'] = Config.access
#app.config['JWT_REFRESH_TOKEN_EXPIRES'] = Config.refresh
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    app.logger.info(f"Trying Login with POST")
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username')
    password = request.json.get('password')
    app.logger.info(f"username:{username}\npassword:{password}")
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    
    # Identity can be any data that is json serializable
    def make_token():
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        app.logger.info(f"access_token:{access_token}\nrefresh_token:{refresh_token}")
        return {'access_token': access_token, 'refresh_token': refresh_token}

    #회원정보 대조
    if username == 'admin' and password == '1234':
        token=make_token()
        return jsonify(access_token=token['access_token'], refresh_token=token['refresh_token'], permission='Landlord'), 200
    elif username == 'guest' and password == '1234':
        token=make_token()
        return jsonify(access_token=token['access_token'], refresh_token=token['refresh_token'], permission='Tenant'), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401


# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route('/refresh', methods=['GET'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify(access_token=access_token, current_user=current_user)


"""
@socketio.on('login')
def handle_message(data):
    app.logger.info(f"Trying Login: {data}")

    #로그인 회원 확인
    message=True

    socketio.emit('response_login', message)
    app.logger.info(f"Sendied message: {message}")
"""
    
@socketio.on('send_message')
def handle_message(message):
    app.logger.info(f"Received message: {message}")

    user_id = message.get('user').get('_id')
    log_entry = {
        'from': user_id,
        'JSON_DATA': message
    }

    logs.append(log_entry)  # 로그 저장
    """
    logging(f"Log: {log_entry}")
    """

    socketio.emit('receive_message', message)
    app.logger.info(f"Sendied message: {message}")


@socketio.on('request_public_key')
def handle_request_public_key(data):
    app.logger.info(f"Received request_public_key: {data}")
    """
    user_id = data.get('user').get('_id')
    log_entry = {
        'from': user_id,
        'JSON_DATA': data
    }

    logs.append(log_entry)  # 로그 저장
    """
    socketio.emit('receive_request_public_key', data)
    app.logger.info(f"Sendied request_public_key: {data}")


@socketio.on('response_public_key')
def handle_public_key(public_key):
    app.logger.info(f"Received response_public_key: {public_key}")
    """
    user_id = public_key.get('user').get('_id')
    log_entry = {
        'from': user_id,
        'JSON_DATA': public_key
    }

    logs.append(log_entry)  # 로그 저장
    """
    socketio.emit('receive_response_public_key', public_key)
    app.logger.info(f"Sendied response_public_key: {public_key}")