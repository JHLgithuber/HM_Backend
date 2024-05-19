from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies, create_refresh_token)
from dotenv import load_dotenv
import ssl
import os

class Connect_to_Frontend:
    def __init__(self,security):
        self.app= Flask(__name__)
        self.socketio = SocketIO(self.app)

        logs = []  # 로그를 저장할 리스트

        if security:
            load_dotenv()
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ssl_context.load_cert_chain(certfile=os.getenv('SSL_CERT'), keyfile=os.getenv('SSL_KEY'), password=os.getenv('SSL_PW'))
            #ssl_context.load_cert_chain(certfile='Key/myserver.crt', keyfile='Key/myserver.key', password=os.getenv('SSL_PW'))
            self.app.run(ssl_context=ssl_context, host='0.0.0.0', port=5000, debug=True)
        else:
            self.app.run(host='0.0.0.0', port=5000, debug=True)

            # 라우트와 소켓 이벤트 핸들러 등록
        self.register_routes()
        self.register_socketio_events()        
        
    def register_routes(self):
        @self.app.route('/')
        def index(self):
            self.app.logger.info('인덱스 페이지에 접근됨')
            return render_template('index.html')

        @self.app.route('/logs')
        def show_logs(self):
            return "LOG:\n"+jsonify(self.logs)

        # Setup the Flask-JWT-Extended extension
        self.app.config['JWT_SECRET_KEY'] = "Config.key"
        #self.app.config['JWT_ACCESS_TOKEN_EXPIRES'] = Config.access
        #self.app.config['JWT_REFRESH_TOKEN_EXPIRES'] = Config.refresh
        jwt = JWTManager(self.app)

        @self.app.route('/login', methods=['POST'])
        def login(self):
            self.app.logger.info(f"Trying Login with POST")
            if not request.is_json:
                return jsonify({"msg": "Missing JSON in request"}), 400

            username = request.json.get('username')
            password = request.json.get('password')
            self.app.logger.info(f"username:{username}\npassword:{password}")
            if not username:
                return jsonify({"msg": "Missing username parameter"}), 400
            if not password:
                return jsonify({"msg": "Missing password parameter"}), 400
            
            # Identity can be any data that is json serializable
            def make_token():
                access_token = create_access_token(identity=username)
                refresh_token = create_refresh_token(identity=username)
                self.app.logger.info(f"access_token:{access_token}\nrefresh_token:{refresh_token}")
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
        @self.app.route('/protected', methods=['GET'])
        @jwt_required
        def protected():
            # Access the identity of the current user with get_jwt_identity
            current_user = get_jwt_identity()
            return jsonify(logged_in_as=current_user), 200


        @self.app.route('/refresh', methods=['GET'])
        @jwt_required(refresh=True)
        def refresh():
            current_user = get_jwt_identity()
            access_token = create_access_token(identity=current_user)
            return jsonify(access_token=access_token, current_user=current_user)

    def register_socketio_events(self):    
        @self.socketio.on('send_message')
        def handle_message(self,message):
            self.app.logger.info(f"Received message: {message}")

            user_id = message.get('user').get('_id')
            log_entry = {
                'from': user_id,
                'JSON_DATA': message
            }

            self.logs.self.append(log_entry)  # 로그 저장
            """
            logging(f"Log: {log_entry}")
            """

            self.socketio.emit('receive_message', message)
            self.app.logger.info(f"Sendied message: {message}")


        @self.socketio.on('request_public_key')
        def handle_request_public_key(self,data):
            self.app.logger.info(f"Received request_public_key: {data}")
            """
            user_id = data.get('user').get('_id')
            log_entry = {
                'from': user_id,
                'JSON_DATA': data
            }

            logs.self.append(log_entry)  # 로그 저장
            """
            self.socketio.emit('receive_request_public_key', data)
            self.app.logger.info(f"Sendied request_public_key: {data}")


        @self.socketio.on('response_public_key')
        def handle_public_key(self,public_key):
            self.app.logger.info(f"Received response_public_key: {public_key}")
            """
            user_id = public_key.get('user').get('_id')
            log_entry = {
                'from': user_id,
                'JSON_DATA': public_key
            }

            logs.self.append(log_entry)  # 로그 저장
            """
            self.socketio.emit('receive_response_public_key', public_key)
            self.app.logger.info(f"Sendied response_public_key: {public_key}")



            