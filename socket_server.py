import socket
import os
import json
import logging
from cryptography.fernet import Fernet

# 로깅 설정
logging.basicConfig(filename='server_connections.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# 암호화 키 생성
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def send_credentials_data():
    host = '192.168.102.19'
    port = 1560
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    logging.info(f"서버가 {host}:{port}에서 클라이언트의 연결을 기다립니다.")
    print(f"서버가 {host}:{port}에서 클라이언트의 연결을 기다립니다.")

    try:
        while True:
            try:
                conn, addr = server_socket.accept()
                logging.info(f"{addr}에서 연결되었습니다.")
                print(f"{addr}에서 연결되었습니다.")
                
                # JSON 파일과 DB 정보 읽기
                with open('server/sturdy-coast-318906-0f9b364f15a4.json', 'r') as file:
                    json_data = file.read()
                
                with open('server/db_info.json', 'r') as db_file:
                    db_info = db_file.read()
                
                # 데이터 암호화
                encrypted_json = cipher_suite.encrypt(json_data.encode('utf-8'))
                encrypted_db_info = cipher_suite.encrypt(db_info.encode('utf-8'))
                
                # 키 수정: 키의 절반을 거꾸로 뒤집어서 뒤에 붙임
                half_key_len = len(key) // 2
                modified_key = key + key[:half_key_len][::-1]
                
                # 데이터 전송
                conn.sendall(modified_key + b'||' + encrypted_json + b'||' + encrypted_db_info)
            except Exception as E:
                logging.error(f"Error: {E}")
            finally:
                conn.close()
    finally:
        server_socket.close()

send_credentials_data()