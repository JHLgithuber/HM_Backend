from ast import Global
import os
import pymysql
from dotenv import load_dotenv

class Connect_to_DB:
    def __init__(self, server):
        self.server = server
        self.index = 0
        self.ID_index = 0
        self.sql = ''''''
        load_dotenv()

        try:
            self.wv_db_connection = pymysql.connect(
                user=os.getenv('DB_ID'),
                passwd=os.getenv('DB_PW'),
                host=os.getenv('DB_HOST'),
                port=int(os.getenv('DB_PORT')),
                db=os.getenv('DB_NAME'),
                charset='utf8'
            )
            self.cursor = self.wv_db_connection.cursor(pymysql.cursors.DictCursor)  # 딕셔너리 형태로 가져옴
            self.server.app.logger.info(f"DB연결 인스턴스 생성됨")
        except pymysql.MySQLError as e:
            self.server.app.logger.error(f"DB 연결 오류: {e}")
            raise ConnectionError(f"Failed to connect to the database: {e}")

    def add_sql(self, sql):
        self.sql += sql
        self.server.app.logger.info(f"추가된 SQL: {sql}\n최종 SQL: {self.sql}")
        return self

    def execute(self):
        try:
            self.cursor.execute(self.sql)
            self.inserted_id = self.cursor.lastrowid
            self.row_count = self.cursor.rowcount
            self.server.app.logger.info(f"SQL 쿼리 실행됨\tinserted_id: {self.inserted_id}\trow_count: {self.row_count}\n SQL: {self.sql}")
        except pymysql.MySQLError as e:
            self.server.app.logger.error(f"SQL 실행 오류: {e}")
            raise RuntimeError(f"Failed to execute SQL query: {e}")
        return self

    def commit(self):
        try:
            self.wv_db_connection.commit()
            self.inserted_id = self.cursor.lastrowid
            self.row_count = self.cursor.rowcount
            self.server.app.logger.info(f"SQL 커밋됨\tinserted_id: {self.inserted_id}\trow_count: {self.row_count}\n SQL: {self.sql}")
        except pymysql.MySQLError as e:
            self.server.app.logger.error(f"SQL 커밋 오류: {e}")
            raise RuntimeError(f"Failed to commit SQL query: {e}")
        return self

    def fetch(self):  # SELECT할때 결과 가져옴
        try:
            self.fetch_data = self.cursor.fetchall()
            self.server.app.logger.info(f"페치됨 fetch_data:\n{self.fetch_data}")
        except pymysql.MySQLError as e:
            self.server.app.logger.error(f"데이터 페치 오류: {e}")
            raise RuntimeError(f"Failed to fetch data: {e}")
        return self

    def get_row_count(self):  # SELECT할때 결과 가져옴
        try:
            self.cursor.execute(self.sql)
            self.inserted_id = self.cursor.lastrowid
            self.row_count = self.cursor.rowcount
            self.server.app.logger.info(f"SQL 쿼리 실행됨\tinserted_id: {self.inserted_id}\trow_count: {self.row_count}\n SQL: {self.sql}")
        except pymysql.MySQLError as e:
            self.server.app.logger.error(f"SQL 실행 오류: {e}")
            raise RuntimeError(f"Failed to execute SQL query: {e}")
        return self.row_count


