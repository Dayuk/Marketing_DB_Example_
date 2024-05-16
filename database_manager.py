# database_manager.py
import pymysql
import logging

class MySQLConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except pymysql.Error as e:
            logging.error("MySQL 데이터베이스 연결 오류: %s", e)
            raise ConnectionError("데이터베이스 연결에 실패했습니다.") from e

    def disconnect(self):
        if self.connection and self.connection.open:
            self.connection.close()

    def execute_query(self, query, data=None):
        if not self.connection or not self.connection.open:
            self.connect()
            if not self.connection.open:
                raise Exception("데이터베이스 재연결 시도 실패")
        try:
            with self.connection.cursor() as cursor:
                if data:
                    cursor.execute(query, data)
                else:
                    cursor.execute(query)
                result = cursor.fetchall()
                self.connection.commit()
                return result
        except pymysql.Error as e:
            try:
                if self.connection.open:
                    self.connection.rollback()
            except pymysql.Error as rollback_error:
                logging.error("롤백 중 오류 발생: %s", rollback_error)
            logging.error("쿼리 실행 오류: %s", e)
            raise DatabaseError("쿼리 실행 실패") from e