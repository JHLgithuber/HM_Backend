# login_class.py
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
import Backend.DBconnect_class as DB_class

class login:
    def __init__(self, server) -> None:
        self.server = server

        self.username = None
        self.password = None
        self.permission = None
        self.access_token = None
        self.refresh_token = None

        self.server.app.logger.info(f"Maked login instance")

    def compare_IDPW(self, username, password):
        # 회원정보 대조
        self.username = username
        self.password = password

        # 임시 회원 인증
        if self.username == 'admin' and self.password == '1234':
            self.make_token()
            self.permission = 'Landlord'
        elif self.username == 'guest' and self.password == '1234':
            self.make_token()
            self.permission = 'Tenant'
        else:
            self.permission = 'Login_Fail'
            self.access_token = None
            self.refresh_token = None

        # 로그인 결과 반환
        self.server.app.logger.info(f"username of instance: {self.username}, password of instance: {self.password}")
        return self

    def make_token(self):
        self.access_token = create_access_token(identity=self.username, additional_claims={"permission": self.permission})
        self.refresh_token = create_refresh_token(identity=self.username)
        self.server.app.logger.info(f"access_token: {self.access_token}, refresh_token: {self.refresh_token}")
        return self

    @jwt_required()
    def protected(self):
        self.username = get_jwt_identity()
        self.code = 200
        return self

    @jwt_required(refresh=True)
    def refresh(self):
        self.username = get_jwt_identity()
        self.access_token = create_access_token(identity=self.username)
        return self
