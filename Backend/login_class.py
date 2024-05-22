# login_class.py
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
import Backend.DBconnect_class as DB_class
from dotenv import load_dotenv

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
        self.server.app.logger.info(f"username of instance: {self.username}, password of instance: {self.password}")

        try:
            self.result=DB_class.Connect_to_DB(self.server).add_sql(f"SELECT PasswordHash,Authority FROM Membership_data WHERE ID = '{self.username}';").execute().fetch().fetch_data
        except Exception as e:
             # 다른 예외가 발생했을 때 실행할 코드
            print("An error occurred:", e)
            self.permission='Login_Fail'
            self.server.app.logger.info(f"Maked login instance")

            # 임시 회원 인증
        if self.username == 'admin' and self.password == '1234':
            self.make_token()
            self.permission = 'Landlord'
        elif self.username == 'guest' and self.password == '1234':
            self.make_token()
            self.permission = 'Tenant'

        
        print(self.result)

        if self.result:
            if self.password==self.result['PasswordHash']:
                self.permission=self.result['Authority']
                self.make_token()
            else:
                self.permission = 'Password mismatch'
                self.access_token = None
                self.refresh_token = None

        else:
            self.permission = 'ID not found'
            self.access_token = None
            self.refresh_token = None


        # 로그인 결과 반환
        self.server.app.logger.info(f"permission of instance: {self.permission}")
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
