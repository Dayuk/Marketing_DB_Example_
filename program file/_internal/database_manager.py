# database_manager.py
import mysql.connector
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
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                auth_plugin='mysql_native_password',
            )
        except mysql.connector.Error as e:
            logging.error("MySQL 데이터베이스 연결 오류: %s", e)
            raise ConnectionError("데이터베이스 연결에 실패했습니다.") from e

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def execute_query(self, query, data=None):
        if not self.connection or not self.connection.is_connected():
            self.connect()
            if not self.connection.is_connected():
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
        except mysql.connector.Error as e:
            try:
                if self.connection.is_connected():
                    self.connection.rollback()
            except mysql.connector.Error as rollback_error:
                logging.error("롤백 중 오류 발생: %s", rollback_error)
            logging.error("쿼리 실행 오류: %s", e)
            raise DatabaseError("쿼리 실행 실패") from e