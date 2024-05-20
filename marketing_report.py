from doctest import FAIL_FAST
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QGridLayout, QStackedWidget, QMainWindow, QSpacerItem, QSizePolicy, QTextBrowser, QTableWidgetItem, QDateEdit
from PyQt5.QtCore import Qt, QPoint, QThread, pyqtSignal, QDateTime
import sys
from uu import Error
import mysql.connector
from functools import partial
import time
from datetime import datetime
import bcrypt
import re
#.py file import
from settings import CREDENTIALS_FILE, SPREADSHEET_NAME, DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE
from sheets_connector import GoogleSheetConnector
from ui_components import FontManager, CustomButtonWithStyle, StyledLineEdit, StyledLabel, StyledTableWidget, StyledComboBox, StyledMessageBox, StyledCompleter, StyledTabWidget, StyledDateEdit
from database_manager import MySQLConnector
from ppt_generator import create_ppt

class InputButtonClicked(CustomButtonWithStyle):
    def __init__(self, main_window, autocompletion_input_field, id_text_field, name_text_field, longtext_text_field, link_text_field, parent=None):
        super(InputButtonClicked, self).__init__("Insert Data", parent)
        self.main_window = main_window
        self.autocompletion_input_field = autocompletion_input_field
        self.id_text_field = id_text_field
        self.name_text_field = name_text_field
        self.longtext_text_field = longtext_text_field
        self.link_text_field = link_text_field
        self.thread = None
        self.is_thread_running = False
        self.clicked.connect(self.start_thread)

    def start_thread(self):
        if self.is_thread_running:
            self.main_window.log_browser.append("이전 작업이 아직 완료되지 않았습니다. 잠시 후 다시 시도해주세요.")
            return
        # 입력 데이터 검증
        self.table_name = self.autocompletion_input_field.text().strip()
        self.id_name = self.id_text_field.text().strip()
        if not self.table_name or not self.id_name:
            self.main_window.log_browser.append("입력 오류: 모든 데이터를 입력해주세요.")
            return
        # 스레드 생성 및 설정
        try:
            self.thread = Worker(self.main_window, self.autocompletion_input_field, self.id_text_field, self.name_text_field, self.longtext_text_field, self.link_text_field)
        except:
            self.main_window.log_browser.append("입력 오류: 데이터를 입력해주세요.")
            return
        # 시그널 연결
        self.is_thread_running = True
        self.thread.result_signal.connect(self.main_window.log_browser.append)  # result 시그널을 로그 브라우저에 연결
        self.thread.finished.connect(self.on_thread_finished)  # 작업 완료 시 중간 메서드 호출

        # 스레드 시작
        self.thread.start()

    def on_thread_finished(self):
        # 스레드가 완전히 종료된 후에 상태 업데이트
        self.is_thread_running = False
        if self.thread.isRunning():
            self.thread.wait()  # 스레드가 완전히 종료될 때까지 기다림
        self.thread.deleteLater()  # 스레드 객체 삭제
        self.main_window.log_browser.append("작업이 완료되었습니다.")

class Worker(QThread):
    finished = pyqtSignal()  # 작업 완료 시그널
    result_signal = pyqtSignal(str)  # 처리 결과를 전달하는 시그널

    def __init__(self, main_window, autocompletion_input_field, id_text_field, name_text_field, longtext_text_field, link_text_field):
        super().__init__()
        self.main_window = main_window
        self.autocompletion_input_field = autocompletion_input_field
        self.id_text_field = id_text_field
        self.name_text_field = name_text_field
        self.longtext_text_field = longtext_text_field
        self.link_text_field = link_text_field

    def run(self):
        self.check_table_existence()

    def check_table_existence(self):
        self.table_name = self.autocompletion_input_field.text().strip()
        
        # 데이터베이스 연결 및 테이블 존재 확인
        self.main_window.mysql_connector.connect()
        try:
            if self.table_name in ["분류", "작업자"]:
                self.result_signal.emit("회사명 Not Found: 타겟이 존재하지 않습니다.")
                return

            query = "SHOW TABLES LIKE %s"
            result = self.main_window.mysql_connector.execute_query(query, (self.table_name,))
            table_exists = bool(result)
            if not table_exists:
                self.result_signal.emit("회사명 Not Found: 타겟이 존재하지 않습니다.")
                return

            # ID와 이름 필드 검증
            id_value = self.id_text_field.text().strip()
            name_value = self.name_text_field.text().strip()
            if not id_value or not name_value:
                self.result_signal.emit("입력 오류: ID와 이름을 모두 입력해주세요.")
                return

            id_query = "SELECT COUNT(*) FROM 분류 WHERE name = %s"
            id_exists = self.main_window.mysql_connector.execute_query(id_query, (id_value,))[0][0] > 0

            name_query = "SELECT COUNT(*) FROM 작업자 WHERE name = %s"
            name_exists = self.main_window.mysql_connector.execute_query(name_query, (name_value,))[0][0] > 0
            self.handle_table_existence_checked(id_exists and name_exists)

        except Error as E:
            error_message = f"데이터베이스 오류 발생: {E}"
            self.result_signal.emit(error_message)
            self.finished.emit()
        finally:
            self.main_window.mysql_connector.disconnect()

    def handle_table_existence_checked(self, exists):
        try:
            if not exists:
                self.result_signal.emit("타겟이 존재하지 않습니다.")
                return
            else:
                self.result_signal.emit("데이터를 삽입 하는 중 입니다.")
            data = [
                self.id_text_field.text(),
                self.name_text_field.text(),
                self.longtext_text_field.text(),
                self.link_text_field.text(),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ]

            # Google Sheets 데이터 삽입
            google_sheets_connector = GoogleSheetConnector(CREDENTIALS_FILE, SPREADSHEET_NAME)
            google_sheets_connector.insert_data(data, self.table_name)

            cursor = self.main_window.mysql_connector
            id_query = "SELECT id, name FROM `분류`"
            results = cursor.execute_query(id_query)
            id_name_map = {name: id for id, name in results}

            # 사용자 입력에 따른 id 검색
            if self.id_text_field.text() in id_name_map:
                self.id_text = id_name_map[self.id_text_field.text()]

            # MySQL 데이터 삽입
            self.main_window.mysql_connector.connect()

            query = f"""
            INSERT INTO {self.table_name} (id, name, text, link, datetime) 
            VALUES (%s, %s, %s, %s, %s)
            """
            data = (self.id_text, self.name_text_field.text(), self.longtext_text_field.text(), self.link_text_field.text(), datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.main_window.mysql_connector.execute_query(query, data)
        finally:
            # 데이터베이스 연결 닫기
            self.main_window.mysql_connector.disconnect()
            self.finished.emit()  # 작업 완료 시그널 발생

class WorkerManager:
    def __init__(self, connector):
        self.connector = connector

    def insert_category_data(self, id, name):
        self.connector.connect()
        cursor = self.connector.connection.cursor()
        try:
            cursor.execute("INSERT INTO 분류 (id, name) VALUES (%s, %s)", (id, name))
            self.connector.connection.commit()
        except mysql.connector.Error as e:
            raise Exception("Failed to insert data: " + str(e))
        finally:
            self.connector.disconnect()

    def load_category_data(self):
        self.connector.connect()
        cursor = self.connector.connection.cursor()
        cursor.execute("SELECT id, name FROM 분류")
        results = cursor.fetchall()
        self.connector.disconnect()
        return results

    def load_workers(self):
        self.connector.connect()
        cursor = self.connector.connection.cursor()
        cursor.execute("SELECT id, name, authority FROM 작업자")
        return cursor.fetchall()

    def update_worker_authority(self, worker_id, new_authority):
        self.connector.connect()
        try:
            with self.connector.connection.cursor() as cursor:
                update_query = "UPDATE 작업자 SET authority = %s WHERE id = %s"
                cursor.execute(update_query, (new_authority, worker_id))
                self.connector.connection.commit()
        finally:
            self.connector.disconnect()

class AutocompletionThread(QThread):
    result = pyqtSignal(list)

    def __init__(self, mysql_connector):
        super(AutocompletionThread, self).__init__()
        self.mysql_connector = mysql_connector

    def run(self):
        try:
            while True:
                self.mysql_connector.connect()

                cursor = self.mysql_connector.connection.cursor()

                cursor.execute("SHOW TABLES")

                table_names = cursor.fetchall()

                # '분류'와 '작업자' 테이블 이름 제외
                table_names = [name[0] for name in table_names if name[0] not in ('분류', '작업자')]

                cursor.execute("SELECT DISTINCT name FROM 분류")
                id_values = cursor.fetchall()

                cursor.execute("SELECT DISTINCT name FROM 작업자")
                name_values = cursor.fetchall()

                id_values = [id[0] for id in id_values]
                name_values = [name[0] for name in name_values]

                autocompletion_data = [table_names] + [id_values] + [name_values]

                self.result.emit(autocompletion_data)

                cursor.close()
                self.mysql_connector.disconnect()

                time.sleep(30)

        except Exception as e:
            self.main_window.log_browser.append(f"Error: {e}")

class FrameWithBar(QFrame):
    def __init__(self, main_window, parent=None):
        super(FrameWithBar, self).__init__(parent)

        self.main_window = main_window

        self.title_bar = QWidget()
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.addStretch(2)

        # Minimize Button
        minimize_button = CustomButtonWithStyle("–", self)
        minimize_button.setObjectName("MinimizeButton")
        minimize_button.setFixedSize(25, 25)
        minimize_button.clicked.connect(self.main_window.showMinimized)
        title_layout.addWidget(minimize_button)

        # Close Button
        close_button = CustomButtonWithStyle("X", self)
        close_button.setObjectName("CloseButton")
        close_button.setFixedSize(25, 25)
        close_button.clicked.connect(self.main_window.close)
        title_layout.addWidget(close_button)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.title_bar)

        self.content_layout = QVBoxLayout()
        self.layout.addLayout(self.content_layout)

        self.setStyleSheet(CustomButtonWithStyle.get_style())

        # 세로 크기 정책 설정
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.setSizePolicy(sizePolicy)

class LoginFrame(QFrame):
    def __init__(self, main_window, parent=None):
        super(LoginFrame, self).__init__(parent)
        self.main_window = main_window  # QMainWindow 인스턴스 저장
        self.setup_ui()

    def setup_ui(self):

        main_layout = QVBoxLayout(self)

        # FrameWithBar 추가
        frame_with_bar = FrameWithBar(self.main_window)
        main_layout.addWidget(frame_with_bar)

        # 로그인 폼을 위한 그리드 레이아웃
        grid_layout = QGridLayout()
        main_layout.addLayout(grid_layout)


        # 레이블과 입력 필드를 튜플 리스트로 정의
        fields = [
            ("ID", StyledLineEdit(self, placeholderText="ID")),
            ("PW", StyledLineEdit(self, placeholderText="PassWord", echoMode=StyledLineEdit.Password))
        ]

        # 그리드 레이아웃에 위젯 추가
        for i, (label_text, line_edit) in enumerate(fields):
            label = StyledLabel(label_text, self)
            grid_layout.addWidget(label, i * 2, 0)  # 레이블 위치 변경
            grid_layout.addWidget(line_edit, i * 2, 1)  # 입력 필드 위치 변경

            # 각 입력 필드 사이에 빈 공간 추가
            if i < len(fields) - 1:
                spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
                grid_layout.addItem(spacer, i * 2 + 1, 0, 1, 2)

        # 로그인 버튼 위에 빈 공간 추가
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        grid_layout.addItem(spacer, len(fields) * 2, 0, 1, 2)

        # 로그인 버튼
        self.login_button = CustomButtonWithStyle("로그인", self)
        self.login_button.clicked.connect(self.handle_login)
        grid_layout.addWidget(self.login_button, len(fields) * 2 + 1, 0, 1, 2)  # 버튼을 두 열에 걸쳐 추가
        self.register_button = CustomButtonWithStyle("계정 생성", self)
        self.register_button.clicked.connect(self.handle_register)
        grid_layout.addWidget(self.register_button, len(fields) * 2 + 2, 0, 1, 2)  # 버튼을 두 열에 걸쳐 추가

    def handle_login(self):
        # 모든 StyledLineEdit 위젯을 찾습니다.
        line_edits = self.findChildren(StyledLineEdit)
        username = None
        password = None

        # 각 입력 필드의 placeholderText를 확인하여 username과 password를 설정합니다.
        for line_edit in line_edits:
            if line_edit.placeholderText() == "ID":
                username = line_edit.text()
            elif line_edit.placeholderText() == "PassWord":
                password = line_edit.text()
        # MySQL 데이터베이스 연결
        self.main_window.mysql_connector.connect()

        try:
            # 사용자 이름과 비밀번호가 일치하는지 확인하는 쿼리 실행
            query = "SELECT pw, name, authority FROM 작업자 WHERE id = %s"
            cursor = self.main_window.mysql_connector.connection.cursor()
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            if result:
                # 데이터베이스에서 가져온 해시된 비밀번호와 입력된 비밀번호 비교
                hashed_password, name, authority = result
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    if authority == 0:
                        StyledMessageBox(self, "로그인 실패", "승인되지 않은 계정입니다.")
                    else:
                        self.main_window.current_user_authority = authority  # 사용자 권한 업데이트
                        self.main_window.switch_to_UI_Frame(2)  # 로그인 성공 시 UI 프레임 전환
                        self.main_window.update_buttons_state(0)
                        # 로그인 성공 후 MainWindow의 name_text 위젯 업데이트
                        self.main_window.set_name_text(name)
                else:
                    StyledMessageBox(self, "로그인 실패", "로그인 정보가 잘못되었습니다.")
            else:
                StyledMessageBox(self, "로그인 실패", "로그인 정보가 잘못되었습니다.")
        except mysql.connector.Error as e:
            StyledMessageBox(self, "로그인 실패", "데이터베이스 오류")
        finally:
            # 데이터베이스 연결 해제
            self.main_window.mysql_connector.disconnect()

    def handle_register(self):
        # 계정 추가 프레임 전환
        self.main_window.switch_to_UI_Frame(1)

class RegisterFrame(QFrame):
    def __init__(self, main_window, parent=None):
        super(RegisterFrame, self).__init__(parent)
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        frame_with_bar = FrameWithBar(self.main_window)
        layout.addWidget(frame_with_bar)

        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)

        fields = [
            ("이름", StyledLineEdit(self, placeholderText="Name")),
            ("ID", StyledLineEdit(self, placeholderText="ID")),
            ("PW", StyledLineEdit(self, placeholderText="PassWord", echoMode=StyledLineEdit.Password))
        ]

        # 그리드 레이아웃에 위젯 추가
        for i, (label_text, line_edit) in enumerate(fields):
            label = StyledLabel(label_text, self)
            grid_layout.addWidget(label, i * 2, 0)  # 레이블 위치 변경
            grid_layout.addWidget(line_edit, i * 2, 1)  # 입력 필드 위치 변경
            line_edit.setObjectName(f"{label_text}_field")  # 입력 필드에 이름 설정

            if i < len(fields) - 1:
                spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
                grid_layout.addItem(spacer, i * 2 + 1, 0, 1, 2)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        grid_layout.addItem(spacer, len(fields) * 2, 0, 1, 2)

        # 생성 버튼
        self.create_button = CustomButtonWithStyle("계정 생성", self)
        self.create_button.clicked.connect(self.create_account)
        grid_layout.addWidget(self.create_button, len(fields) * 2 + 1, 0, 1, 2)  # 버튼을 두 열에 걸쳐 추가
        self.cancel_button = CustomButtonWithStyle("취소", self)
        self.cancel_button.clicked.connect(self.cancel)
        grid_layout.addWidget(self.cancel_button, len(fields) * 2 + 2, 0, 1, 2)  # 버튼을 두 열에 걸쳐 추가

    def cancel(self):
        self.main_window.switch_to_UI_Frame(0)

    def create_account(self):
        # 입력 필드에서 사용자 이름, ID, 비밀번호 가져오기
        name = self.findChild(StyledLineEdit, "이름_field").text()
        user_id = self.findChild(StyledLineEdit, "ID_field").text().lower()  # 대문자를 소문자로 변환
        password = self.findChild(StyledLineEdit, "PW_field").text()

        # 모든 필드가 채워졌는지 확인
        if not name or not user_id or not password:
            StyledMessageBox(self, "계정 생성 실패", "모든 정보를 입력해주세요.")
            return

        # 사용자 ID 길이 검증
        if len(user_id) > 20:
            StyledMessageBox(self, "계정 생성 실패", "ID는 20자 이하로 입력해주세요.")
            return

        # 이름 길이 제한 및 한국어 여부 확인
        if len(name) > 5:
            StyledMessageBox(self, "계정 생성 실패", "이름은 5자 이내로 입력해주세요.")
            return
        if not re.match("^[가-힣]+$", name):
            StyledMessageBox(self, "계정 생성 실패", "이름은 한국어로만 입력해주세요.")
            return
        # user_id 유효성 검사 (소문자 영문자와 숫자만 허용)
        if not re.match("^[a-z0-9]+$", user_id):
            StyledMessageBox(self, "계정 생성 실패", "ID는 영어와 숫자만 사용할 수 있습니다.")
            return

        # 비밀번호를 바이트로 인코딩하고 bcrypt로 해싱
        password_bytes = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

        # MySQL 데이터베이스 연결
        self.main_window.mysql_connector.connect()

        try:
            with self.main_window.mysql_connector.connection.cursor() as cursor:
                # 사용자 계정을 생성하는 SQL 쿼리
                sql = "INSERT INTO 작업자 (name, id, pw, authority) VALUES (%s, %s, %s, %s)"
                # 실행
                cursor.execute(sql, (name, user_id, hashed_password, 0))
                # 변경사항 저장
                self.main_window.mysql_connector.connection.commit()
                StyledMessageBox(self, "계정 생성 성공", "새로운 계정이 성공적으로 생성되었습니다.\n관리자에게 승인을 요청해주세요.")
        except mysql.connector.Error as e:
            StyledMessageBox(self, "계정 생성 실패", "데이터베이스 오류")
        finally:
            # 데이터베이스 연결 해제
            self.main_window.mysql_connector.disconnect()

        # 로그인 페이지로 돌아가기
        self.main_window.switch_to_UI_Frame(0)
        self.findChild(StyledLineEdit, "이름_field").clear()
        self.findChild(StyledLineEdit, "ID_field").clear()
        self.findChild(StyledLineEdit, "PW_field").clear()

class WorkerFrame(QFrame):
    def __init__(self, main_window, worker_manager):
        super(WorkerFrame, self).__init__(main_window)  # main_window를 부모로 설정
        self.main_window = main_window  # main_window 참조를 내부 속성으로 저장
        self.worker_manager = worker_manager
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        frame_with_bar = FrameWithBar(self.main_window)
        layout.addWidget(frame_with_bar)
        self.tab_widget = StyledTabWidget()  # 탭 위젯 생성
        layout.addWidget(self.tab_widget)

        # 기존 Worker 관리 탭
        self.manage_workers_tab = QWidget()
        self.tab_widget.addTab(self.manage_workers_tab, "계정 권한")
        self.setup_workers_tab()

        # 분류 테이블 데이터 탭
        self.category_tab = QWidget()
        self.tab_widget.addTab(self.category_tab, "작업 분류")
        self.setup_category_tab()

    def setup_workers_tab(self):
        layout = QVBoxLayout(self.manage_workers_tab)
        self.worker_table = StyledTableWidget(0, 3)
        self.worker_table.setHorizontalHeaderLabels(["ID", "Name", "Authority"])
        layout.addWidget(self.worker_table)
        self.authority_combo = StyledComboBox()
        self.authority_combo.addItems(["미승인", "Admin", "승인"])
        update_button = CustomButtonWithStyle("권한 업데이트")
        update_button.clicked.connect(self.update_authority)

        update_layout = QHBoxLayout()
        update_layout.addWidget(StyledLabel("설정 권한:"))
        update_layout.addWidget(self.authority_combo)
        update_layout.addWidget(update_button)
        layout.addLayout(update_layout)

        self.load_workers()

    def setup_category_tab(self):
        layout = QVBoxLayout(self.category_tab)
        self.category_table = StyledTableWidget(0, 2)  # 2열(id, name) 테이블
        self.category_table.setHorizontalHeaderLabels(["ID", "Name"])
        layout.addWidget(self.category_table)

        input_layout = QHBoxLayout()
        self.id_input = StyledLineEdit(self, placeholderText="ID")
        self.name_input = StyledLineEdit(self, placeholderText="Name")
        input_layout.addWidget(StyledLabel("ID:"))
        input_layout.addWidget(self.id_input)
        input_layout.addWidget(StyledLabel("Name:"))
        input_layout.addWidget(self.name_input)
        # 행 추가 버튼
        add_row_button = CustomButtonWithStyle("Add Row")
        add_row_button.clicked.connect(self.add_row_to_category_table)
        input_layout.addWidget(add_row_button)

        layout.addLayout(input_layout)

        self.load_category_data()

    def load_category_data(self):
        results = self.worker_manager.load_category_data()  # 분류 데이터 로드
        self.category_table.setRowCount(0)
        for row_number, row_data in enumerate(results):
            self.category_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.category_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def add_row_to_category_table(self):
        id_text = self.id_input.text()
        name_text = self.name_input.text()

        # 입력 검증
        if not id_text or not name_text:
            StyledMessageBox(self, "Input Error", "ID와 NAME을 모두 입력해주세요.")
            return

        # 데이터베이스에 삽입
        try:
            self.worker_manager.insert_category_data(id_text, name_text)
            self.load_category_data()  # 테이블 데이터 갱신
            self.id_input.clear()  # 입력 필드 초기화
            self.name_input.clear()
            StyledMessageBox(self, "데이터가 정상적으로 입력되었습니다.")
        except Exception as e:
            StyledMessageBox(self, "Database Error", str(e))

    def load_workers(self):
        results = self.worker_manager.load_workers()
        self.worker_table.setRowCount(0)
        for row_number, row_data in enumerate(results):
            self.worker_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.worker_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def update_authority(self):
        selected_row = self.worker_table.currentRow()
        if selected_row == -1:
            StyledMessageBox(self, "Selection Error", "권한을 변경할 계정을 선택해주세요.")
            return

        worker_id = self.worker_table.item(selected_row, 0).text()
        new_authority = self.authority_combo.currentIndex()
        self.worker_manager.update_worker_authority(worker_id, new_authority)
        StyledMessageBox(self, "Update Success", "권한이 성공적으로 변경되었습니다.")
        self.load_workers()

class TableViewFrame(QFrame):
    def __init__(self, main_window, mysql_connector):
        super(TableViewFrame, self).__init__(main_window)
        self.main_window = main_window  # main_window 참조를 내부 속성으로 저장
        self.mysql_connector = mysql_connector
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        frame_with_bar = FrameWithBar(self.main_window)
        layout.addWidget(frame_with_bar)
        self.table_widget = StyledTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["회사명", "분류"])
        layout.addWidget(self.table_widget)
        self.load_data()

    def load_data(self):
        self.mysql_connector.connect()
        cursor = self.mysql_connector.connection.cursor()
        try:
            # 모든 테이블 이름 가져오기
            cursor.execute("SHOW TABLES FROM my_database")
            tables = cursor.fetchall()

            # 분류 테이블의 name 컬럼 가져오기
            cursor.execute("SELECT name FROM 분류")
            categories = cursor.fetchall()

            # 필터링: '분류'와 '작업자' 테이블 이름 제외
            filtered_tables = [table for table in tables if table[0] not in ('분류', '작업자')]

            self.table_widget.setRowCount(max(len(filtered_tables), len(categories)))

            for i, table in enumerate(filtered_tables):
                self.table_widget.setItem(i, 0, QTableWidgetItem(table[0]))

            for i, category in enumerate(categories):
                self.table_widget.setItem(i, 1, QTableWidgetItem(category[0]))

        except mysql.connector.Error as e:
            StyledMessageBox(self, "데이터 로드 실패", str(e))
        finally:
            cursor.close()
            self.mysql_connector.disconnect()

class ExportPPTFrame(QFrame):
    def __init__(self, main_window):
        super(ExportPPTFrame, self).__init__(main_window)  # main_window를 부모로 설정
        self.main_window = main_window  # main_window 참조를 내부 속성으로 저장
        self.setup_ui()

    def setup_ui(self):
        layout = QGridLayout(self)
        frame_with_bar = FrameWithBar(self.main_window)
        frame_with_bar.setFixedHeight(55)
        layout.addWidget(frame_with_bar, 0, 1, 1, 3)  # 첫 번째 행에 프레임 추가

        # 회사명 레이블과 입력 필드
        layout.addWidget(StyledLabel("회사명:"), 1, 0)  # 레이블 위치 설정
        self.company_name_input = StyledLineEdit(self, placeholderText="회사명을 입력해주세요")
        layout.addWidget(self.company_name_input, 1, 1)  # 입력 필드 위치 설정

        # 확인 버튼 추가
        self.confirm_button = CustomButtonWithStyle("확인")
        self.confirm_button.clicked.connect(self.confirm_company_name)
        layout.addWidget(self.confirm_button, 1, 2)  # 버튼 위치 설정

        # 시작 날짜 선택
        self.start_date_edit = StyledDateEdit(self)
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDateTime(QDateTime.currentDateTime())
        layout.addWidget(StyledLabel("시작 날짜:"), 2, 0)
        layout.addWidget(self.start_date_edit, 2, 1)

        # 종료 날짜 선택
        self.end_date_edit = StyledDateEdit(self)
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDateTime(QDateTime.currentDateTime())
        layout.addWidget(StyledLabel("종료 날짜:"), 3, 0)
        layout.addWidget(self.end_date_edit, 3, 1)

        # Export 버튼
        export_button = CustomButtonWithStyle("Export PPT")
        export_button.clicked.connect(self.export_ppt)
        layout.addWidget(export_button, 4, 0, 1, 3)  # Export 버튼을 세 열에 걸쳐 추가

    def confirm_company_name(self):
        self.company_name_input.setEnabled(False)
        self.confirm_button.setEnabled(False)
        company_name = self.company_name_input.text().strip()
        if not company_name:
            self.main_window.log_browser.append("입력 오류 회사명을 입력해주세요.")
            self.company_name_input.setEnabled(True)
            self.confirm_button.setEnabled(True)
            return

        self.main_window.mysql_connector.connect()
        try:
            query = "SELECT MIN(datetime), MAX(datetime) FROM `{}`".format(company_name)
            cursor = self.main_window.mysql_connector.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            if result and result[0] and result[1]:
                min_date, max_date = result
                self.start_date_edit.setMinimumDate(min_date.date())
                self.start_date_edit.setMaximumDate(max_date.date())
                self.start_date_edit.setDate(min_date.date())
                self.end_date_edit.setMinimumDate(min_date.date())
                self.end_date_edit.setMaximumDate(max_date.date())
                self.end_date_edit.setDate(max_date.date())
                self.main_window.log_browser.append("시작 및 종료 날짜가 설정되었습니다.\nstart date: " + min_date.date().strftime('%Y-%m-%d') + "\nend date: " + max_date.date().strftime('%Y-%m-%d'))
        except mysql.connector.Error:
            self.main_window.log_browser.append("데이터가 올바르지 않거나 데이터베이스의 연결이 원활하지 않습니다.")
            self.company_name_input.setEnabled(True)
            self.confirm_button.setEnabled(True)
        finally:
            self.main_window.mysql_connector.disconnect()

    def export_ppt(self):
        company_name = self.company_name_input.text()
        start_date = self.start_date_edit.date()
        end_date = self.end_date_edit.date()
        
        if start_date > end_date:
            self.main_window.log_browser.append("날짜 오류: 시작 날짜가 종료 날짜보다 늦을 수 없습니다.")
            self.company_name_input.setEnabled(True)
            self.confirm_button.setEnabled(True)
            return
        
        company_name = self.company_name_input.text().strip()
        if not company_name:
            self.main_window.log_browser.append("입력 오류: 회사명을 입력해주세요.")
            self.company_name_input.setEnabled(True)
            self.confirm_button.setEnabled(True)
            return
        
        try:
            if start_date > end_date:
                self.main_window.log_browser.append("날짜 오류: 시작 날짜가 종료 날짜보다 늦을 수 없습니다.")
                return
            
            if not company_name:
                self.main_window.log_browser.append("입력 오류: 회사명을 입력해주세요.")
                return
        
            # QDate 객체를 문자열로 변환
            start_date_str = start_date.toString('yyyy-MM-dd')
            end_date_str = end_date.toString('yyyy-MM-dd')

            # 데이터베이스에서 데이터 가져오기
            data = self.fetch_data(company_name, start_date, end_date)
            
            # PPT 생성
            ppt_file = create_ppt(company_name, data, start_date_str, end_date_str)
            self.main_window.log_browser.append(f"PPT가 생성되었습니다: {ppt_file}")
            pass
        finally:
            self.company_name_input.setEnabled(True)
            self.confirm_button.setEnabled(True)
            self.company_name_input.clear()
            self.start_date_edit.clear()
            self.end_date_edit.clear()

    def fetch_data(self, company_name, start_date, end_date):
        # QDate 객체를 'YYYY-MM-DD' 형식의 문자열로 변환
        start_date_str = start_date.toString('yyyy-MM-dd')
        end_date_str = end_date.toString('yyyy-MM-dd')

        query = f"""
                SELECT id, name, text, link, datetime
                FROM `{company_name}`
                WHERE datetime BETWEEN '{start_date_str}' AND '{end_date_str}'
                """
        try:
            self.main_window.mysql_connector.connect()
            cursor = self.main_window.mysql_connector.connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            return data
        except mysql.connector.Error as e:
            print(e)
            self.main_window.log_browser.append(f"데이터베이스 오류: {str(e)}")
            return []
        finally:
            cursor.close()
            self.main_window.mysql_connector.disconnect()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.current_user_authority = None  # 사용자 권한을 저장할 속성 추가
        # Google Sheet 연결 정보
        self.google_sheet_connector = GoogleSheetConnector(CREDENTIALS_FILE, SPREADSHEET_NAME)
        # MySQL 연결 정보
        self.mysql_connector = MySQLConnector(DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE)
        self.worker_manager = WorkerManager(self.mysql_connector)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
                            background-color: #292929; 
                            color: white; 
                            border-radius: 8px;
                            """)

        self.setWindowTitle("Example Program")

        main_layout = QVBoxLayout()

        frame_with_bar = FrameWithBar(self)
        self.login_frame = LoginFrame(self)
        self.register_frame = RegisterFrame(self)

        main_layout.addWidget(frame_with_bar)

        self.central_widget = QFrame()
        main_layout.addWidget(self.central_widget)

        self.frame_list = QHBoxLayout()
        self.frame_list.addWidget(self.login_frame)
        self.frame_list.addWidget(self.register_frame)
        self.frame_list.addWidget(self.central_widget)

        self.ui_central_widget = QFrame()
        self.ui_central_widget.setLayout(self.frame_list)
        self.setCentralWidget(self.ui_central_widget)

        self.switch_to_UI_Frame(0)
        
        central_layout = QHBoxLayout(self.central_widget)

        # 프레임 전환 버튼 추가
        self.frame_buttons_layout = QVBoxLayout()  # 프레임 전환 버튼을 세로로 정렬하기 위해 QVBoxLayout 사용

        self.frame_buttons = []  # 각 프레임의 프레임 전환 버튼을 저장할 리스트
        button_name = ["Input Data", "Table Viewer", "Management", "Export PPT"]
        for i in range(4):
            button = CustomButtonWithStyle(button_name[i])
            button.clicked.connect(partial(self.switch_to_frame, i))
            self.frame_buttons_layout.addWidget(button)
            self.frame_buttons.append(button)  # 프레임 전환 버튼을 리스트에 추가

        central_layout.addLayout(self.frame_buttons_layout)

        # 스택 위젯 생성
        self.stacked_widget = QStackedWidget()
        central_layout.addWidget(self.stacked_widget)

        # 로그 출력 브라우저 생성
        self.log_browser_Layout = QVBoxLayout()
        self.log_browser = QTextBrowser()
        self.log_browser.setFont(FontManager(font_size=10).get_font())  # 폰트 설정
        self.log_browser.setStyleSheet("border: 2px solid white; border-radius: 8px; width: 110px;")
        self.log_browser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 스크롤바 없애기
        self.log_browser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 스크롤바 없애기
        self.log_browser_label = StyledLabel("Log")
        self.log_browser_Layout.addWidget(self.log_browser_label)
        self.log_browser_Layout.addWidget(self.log_browser)
        central_layout.addLayout(self.log_browser_Layout)

        # 프레임 생성 및 스택 위젯에 추가
        self.frames = []
        for i in range(4):
            if i == 1:
                # TableViewFrame을 2번째 프레임으로 추가
                self.table_view_frame = TableViewFrame(self, self.mysql_connector)
                self.stacked_widget.addWidget(self.table_view_frame)
                self.frames.append(self.table_view_frame)
            elif i == 2:
                # WorkerFrame을 3번째 프레임으로 추가
                self.worker_frame = WorkerFrame(self, self.worker_manager)
                self.stacked_widget.addWidget(self.worker_frame)
                self.frames.append(self.worker_frame)
            elif i == 3:
                self.export_ppt_frame = ExportPPTFrame(self)
                self.stacked_widget.addWidget(self.export_ppt_frame)
                self.frames.append(self.export_ppt_frame)
            else:
                frame = FrameWithBar(self)
                grid_layout = QGridLayout()
                frame.content_layout.addLayout(grid_layout)
                autocompletion_input_label = StyledLabel("회사명")
                self.autocompletion_input_field = StyledLineEdit(self, placeholderText="회사명을 입력해주세요")
                grid_layout.addWidget(autocompletion_input_label, 0, 0)  # input label을 왼쪽에 배치
                grid_layout.addWidget(self.autocompletion_input_field, 0, 1)  # input field를 오른쪽에 배치

                self.id_text = StyledLineEdit(self, placeholderText="작업 종류를 입력해주세요")
                self.name_text = StyledLineEdit(self, placeholderText="작업자 이름")
                self.longtext_text = StyledLineEdit(self)
                self.link_text = StyledLineEdit(self)

                inputs = {
                    "분류": self.id_text,
                    "작업자": self.name_text,
                    "내용": self.longtext_text,
                    "Link": self.link_text
                }

                for g, (label_text, input_widget) in enumerate(inputs.items(), start=1):
                    label = StyledLabel(label_text)
                    input_widget.setObjectName(f"{label_text}_field")
                    grid_layout.addWidget(label, g, 0)
                    grid_layout.addWidget(input_widget, g, 1)

                self.stacked_widget.addWidget(frame)
                self.frames.append(frame)

                # input_label과 button_layout 사이에 수평 스페이서 추가
                spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
                frame.content_layout.addItem(spacer)

                # 프레임에 버튼 추가
                button_layout = QHBoxLayout()  # 버튼을 가로로 정렬하기 위해 QHBoxLayout 사용
                frame.content_layout.addLayout(button_layout)

                if i == 0:
                    button = InputButtonClicked(self, self.autocompletion_input_field, self.id_text, self.name_text,
                                                self.longtext_text, self.link_text)
                    button.setText("Input Data")
                    button_layout.addWidget(button)
                else:
                    button = CustomButtonWithStyle(f"Button 1")
                    button_layout.addWidget(button)

        # 배경색 지정
        self.central_widget.setStyleSheet("background-color: #292929; color: white;")

        # 현재 보이는 프레임의 버튼은 보이지만 누를 수 없도록 설정
        self.stacked_widget.currentChanged.connect(self.update_buttons_state)

        # AutocompletionThread 초기화 및 시작
        self.autocompletion_thread = AutocompletionThread(self.mysql_connector)
        self.autocompletion_thread.result.connect(self.update_completer)
        self.autocompletion_thread.start()

    def set_name_text(self, text):
        # 첫 번째 프레임에서 self.name_text 찾기
        name_text_widget = self.frames[0].findChild(StyledLineEdit, "작업자_field")
        if name_text_widget:
            name_text_widget.setText(text)
            name_text_widget.setReadOnly(True)

    def switch_to_UI_Frame(self, index):
        # 모든 프레임을 숨깁니다.
        for i in range(self.frame_list.count()):
            frame = self.frame_list.itemAt(i).widget()
            if frame is not None:
                frame.hide()

        # 지정된 인덱스의 프레임만 보이게 합니다.
        frame_to_show = self.frame_list.itemAt(index).widget()
        frame_to_show.show()

    def update_completer(self, autocompletion_data):
        completer = StyledCompleter(autocompletion_data[0], self)
        self.export_ppt_frame.company_name_input.setCompleter(completer)
        input_fields = self.frames[0].findChildren(StyledLineEdit)
        for index, data in enumerate(autocompletion_data):
            completer = StyledCompleter(data, self)
            input_field = input_fields[index]
            if input_field == self.name_text:
                continue  # name_text에는 자동완성 설정을 적용하지 않음
            input_field.setCompleter(completer)

    def switch_to_frame(self, index):
        if str(index).isdigit():
            self.stacked_widget.setCurrentIndex(int(index))

    def update_buttons_state(self, index):
        # 모든 버튼을 일단 활성화
        for button in self.frame_buttons:
            button.setEnabled(True)
        
        # 현재 인덱스의 버튼만 비활성화
        if index < len(self.frame_buttons):
            self.frame_buttons[index].setEnabled(False)
        
        # "Management" 버튼은 authority에 따라 항상 관리
        if hasattr(self, 'current_user_authority'):
            self.frame_buttons[2].setVisible(self.current_user_authority == 1)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())