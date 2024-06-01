import json
import logging
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt, unset_jwt_cookies, create_refresh_token
)
from dotenv import load_dotenv
import ssl
import os


import Backend.mgmt_class as mgmt_class
import Backend.login_class as login_class


class Connect_to_Frontend:
    def __init__(self, security):
        load_dotenv()
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)
        self.showing_logs = []  # 로그를 저장할 리스트

        # 로깅 설정
        logging.basicConfig(level=logging.INFO)
        self.app.logger.setLevel(logging.INFO)
        self.app.logger.info('서버 시작됨')

        # JWT 설정
        self.app.config['JWT_SECRET_KEY'] = "your_jwt_secret_key"  # 환경 변수로 대체하는 것이 좋습니다.
        self.jwt = JWTManager(self.app)

        self.register_routes()
        self.register_socketio_events()

        if security:
            load_dotenv()
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ssl_context.load_cert_chain(
                certfile=os.getenv('SSL_CERT'),
                keyfile=os.getenv('SSL_KEY'),
                password=os.getenv('SSL_PW')
            )
            self.app.run(ssl_context=ssl_context, host='0.0.0.0', port=5000, debug=True)
        else:
            self.app.run(host='0.0.0.0', port=5000, debug=True)

    def register_routes(self):
        @self.app.route('/')
        def index():
            self.app.logger.info('인덱스 페이지에 접근됨')
            return render_template('index.html')

        @self.app.route('/logs')
        def showing_logs():
            self.app.logger.info('로그 페이지에 접근됨')
            return "Server Log:\n" + json.dumps(self.showing_logs, indent=4)

        @self.app.route('/login', methods=['POST'])
        def login():
            self.app.logger.info("Trying Login with POST")
            if not request.is_json:
                return jsonify({"msg": "Missing JSON in request"}), 400

            username = request.json.get('username')
            password = request.json.get('password')
            self.app.logger.info(f"username: {username}, password: {password}")

            if not username:
                return jsonify({"msg": "Missing username parameter"}), 400
            if not password:
                return jsonify({"msg": "Missing password parameter"}), 400

            login_result = login_class.login(self).compare_IDPW(username, password)

            if login_result.permission not in ['Login_Fail', 'ID not found', 'Password mismatch']:
                return jsonify(
                    access_token=login_result.access_token,
                    refresh_token=login_result.refresh_token,
                    permission=login_result.permission
                ), 200
            else:
                return jsonify({"msg": "Bad username or password"}), 401

        @self.app.route('/protected', methods=['GET'])
        @jwt_required()
        def protected():
            current_user = get_jwt_identity()
            permission = get_jwt().get('permission', None)
            return jsonify(logged_in_as=current_user, permission=permission), 200

        @self.app.route('/refresh', methods=['GET'])
        @jwt_required(refresh=True)
        def refresh():
            current_user = get_jwt_identity()
            access_token = create_access_token(identity=current_user)
            return jsonify(access_token=access_token, current_user=current_user)

    def jwt_checked(self, access_token):
        if access_token:
            with self.app.app_context():
                user_identity = None
                permission = None
                try:
                    # 임시 요청 컨텍스트를 만들어 JWT 토큰에서 클레임 추출
                    from flask_jwt_extended import decode_token
                    decoded_token = decode_token(access_token)
                    user_identity = decoded_token['sub']
                    permission = decoded_token['permission']
                except Exception as e:
                    self.app.logger.error(f"Error decoding JWT: {e}")
        self.app.logger.info(f"User identity: {user_identity}, Permission: {permission}")
        return {'user_identity': user_identity,'permission': permission}


    def register_socketio_events(self):
        @self.socketio.on('read_data')
        def handle_request_data(message):
            sid = request.sid
            self.app.logger.info(f"Received message: {message}")
            
            # JWT 토큰 검증 및 클레임 추출
            jwd_checked_data=self.jwt_checked(message.get('access_token'))

            try:
                response_data = mgmt_class.Mgmt(id=jwd_checked_data['user_identity'], CURD='read',
                                                entity=message.get('entity'), where=message.get('where'),
                                                option=message.get('option'), data=None, server=self,
                                                permission=jwd_checked_data['permission']).result   #DB자료 없을때 예외처리 필요
                print(response_data)
            except Exception as e:
                self.app.logger.error(f"Error mgmt data in DB: {e}")


            log_entry = {
                'SID': sid,
                'ID': jwd_checked_data['user_identity'],
                'Requested_data': message.get('entity'),
                'Responsed_data': response_data,
                'ALL_JSON_DATA': message
            }

            self.showing_logs.append(log_entry)  # 로그 저장
            self.socketio.emit('responsed_data', json.dumps(response_data), to=sid)
            #self.socketio.emit('receive_message', log_entry)
            self.app.logger.info(f"Sent message: {message} to {sid}")

        @self.socketio.on('update_data')
        def handle_update_data(message):
            sid = request.sid
            self.app.logger.info(f"Received message: {message}")

            # JWT 토큰 검증 및 클레임 추출
            jwd_checked_data = self.jwt_checked(message.get('access_token'))

            try:
                response_data = mgmt_class.Mgmt(id=jwd_checked_data['user_identity'], CURD='update',
                                                entity=message.get('entity'), where=message.get('where'),
                                                option=message.get('option'), data=message.get('data'), server=self,
                                                permission=jwd_checked_data['permission']).result  # DB자료 없을때 예외처리 필요
                print(response_data)
            except Exception as e:
                self.app.logger.error(f"Error mgmt data in DB: {e}")

            log_entry = {
                'SID': sid,
                'ID': jwd_checked_data['user_identity'],
                'Requested_data': message.get('entity'),
                'Responsed_data': response_data,
                'ALL_JSON_DATA': message
            }

            self.showing_logs.append(log_entry)  # 로그 저장
            self.socketio.emit('responsed_data', json.dumps(response_data), to=sid)
            # self.socketio.emit('receive_message', log_entry)
            self.app.logger.info(f"Sent message: {message} to {sid}")

        @self.socketio.on('create_data')
        def handle_create_data(message):
            sid = request.sid
            self.app.logger.info(f"Received message: {message}")

            # JWT 토큰 검증 및 클레임 추출
            jwd_checked_data = self.jwt_checked(message.get('access_token'))

            try:
                response_data = mgmt_class.Mgmt(id=jwd_checked_data['user_identity'], CURD='create',
                                                entity=message.get('entity'), where=message.get('where'),
                                                option=message.get('option'), data=message.get('data'), server=self,
                                                permission=jwd_checked_data['permission']).result  # DB자료 없을때 예외처리 필요
                print(response_data)
            except Exception as e:
                self.app.logger.error(f"Error mgmt data in DB: {e}")

            log_entry = {
                'SID': sid,
                'ID': jwd_checked_data['user_identity'],
                'Requested_data': message.get('entity'),
                'Responsed_data': response_data,
                'ALL_JSON_DATA': message
            }

            self.showing_logs.append(log_entry)  # 로그 저장
            self.socketio.emit('responsed_data', json.dumps(response_data), to=sid)
            # self.socketio.emit('receive_message', log_entry)
            self.app.logger.info(f"Sent message: {message} to {sid}")

        @self.socketio.on('delete_data')
        def handle_delete_data(message):
            sid = request.sid
            self.app.logger.info(f"Received message: {message}")

            # JWT 토큰 검증 및 클레임 추출
            jwd_checked_data = self.jwt_checked(message.get('access_token'))

            try:
                response_data = mgmt_class.Mgmt(id=jwd_checked_data['user_identity'], curd='delete',
                                                entity=message.get('entity'), where=message.get('where'),
                                                option=message.get('option'), data=message.get('data'), server=self,
                                                permission=jwd_checked_data['permission']).result  # DB자료 없을때 예외처리 필요
                print(response_data)
            except Exception as e:
                self.app.logger.error(f"Error mgmt data in DB: {e}")

            log_entry = {
                'SID': sid,
                'ID': jwd_checked_data['user_identity'],
                'Requested_data': message.get('entity'),
                'Responsed_data': response_data,
                'ALL_JSON_DATA': message
            }

            self.showing_logs.append(log_entry)  # 로그 저장
            self.socketio.emit('responsed_data', json.dumps(response_data), to=sid)
            # self.socketio.emit('receive_message', log_entry)
            self.app.logger.info(f"Sent message: {message} to {sid}")

        @self.socketio.on('send_message')
        def handle_message(message):
            client = request.sid
            self.app.logger.info(f"Received message: {message}")
            user_id = message.get('user').get('_id')
            log_entry = {
                'from': user_id,
                'JSON_DATA': message
            }
            self.showing_logs.append(log_entry)  # 로그 저장
            self.socketio.emit('receive_message', message, to=client)
            self.socketio.emit('receive_message', log_entry)
            self.app.logger.info(f"Sent message: {message} to {client}")
