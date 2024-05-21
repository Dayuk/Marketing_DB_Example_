# settings.py 파일에 상수 정의
import socket
import json
from google.oauth2 import service_account
from cryptography.fernet import Fernet

def receive_credentials_and_authenticate():
    host = '192.168.102.19'
    port = 1560
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    # 데이터 수신
    received_data = client_socket.recv(4096)
    print(received_data)
    modified_key, encrypted_json, encrypted_db_info = received_data.split(b'||')
    
    # 키 수정: 원래 키를 복원
    half_key_len = len(modified_key) // 3  # 전체 길이의 1/3이 원래 키의 절반 길이
    original_key = modified_key[:2 * half_key_len]  # 원래 키 추출
    
    # 암호화 해제
    cipher_suite = Fernet(original_key)
    json_data = cipher_suite.decrypt(encrypted_json).decode('utf-8')
    db_info = cipher_suite.decrypt(encrypted_db_info).decode('utf-8')
    
    # JSON 문자열을 딕셔너리로 변환
    credentials_info = json.loads(json_data)
    db_credentials = json.loads(db_info)
    
    # 서비스 계정 키 생성 및 스코프 지정
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=scopes)
    
    client_socket.close()
    return credentials, db_credentials

credentials_file, db_credentials = receive_credentials_and_authenticate()

MAX_ROWS = 1000
MAX_COLS = 7
CREDENTIALS_FILE = credentials_file
SPREADSHEET_NAME = 'Example_Spread_Sheet'
DB_HOST = '192.168.102.19'
DB_USER = db_credentials['DB_USER']
DB_PASSWORD = db_credentials['DB_PASSWORD']
DB_DATABASE = 'my_database'
FONT_PATH = "NotoSansKR-Medium.ttf"
