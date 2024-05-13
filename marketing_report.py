from pickle import NONE
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QLineEdit, QGridLayout, QMessageBox, QStackedWidget, QMainWindow, QSpacerItem, QSizePolicy, QCompleter
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt, QPoint, QThread, pyqtSignal, QObject
import pymysql
from functools import partial
import time
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
from settings import MAX_ROWS, MAX_COLS, CREDENTIALS_FILE, SPREADSHEET_NAME, DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class CustomButtonWithStyle(QPushButton):
    def __init__(self, text, parent=None):
        super(CustomButtonWithStyle, self).__init__(text, parent)
        self.init_ui()

    def init_ui(self):
        # 폰트 설정
        font_id = QFontDatabase.addApplicationFont("NotoSansKR-Medium.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 16)
        self.setFont(font)

        # 버튼 스타일 설정
        self.setStyleSheet(self.get_style())

    @staticmethod
    def get_style():
        # 버튼 및 타이틀 바 스타일 정의
        return """
            QPushButton {
                background-color: #292929;
                color: white;
                border: 2px solid white;
                border-radius: 8px;
                padding: 10px 24px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: white;
                color: #292929;
                border: 2px solid #292929;
            }
            QPushButton:disabled {
                background-color: white;
                color: #292929;
                border: 2px solid #292929;
            }
            QPushButton#MinimizeButton, QPushButton#CloseButton {
                background-color: #292929;
                color: white;
                border: 2px solid white;
                border-radius: 8px;
                padding: 0px;
                font-size: 12px;
            }
            QPushButton#MinimizeButton:hover, QPushButton#CloseButton:hover {
                background-color: white;
                color: #292929;
            }
            QPushButton#MinimizeButton:disabled, QPushButton#CloseButton:disabled {
                background-color: white;
                color: #292929;
            }
        """

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
        if not self.connection:
            raise Exception("데이터베이스 연결이 없습니다.")
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
            self.connection.rollback()
            logging.error("쿼리 실행 오류: %s", e)
            raise Exception("쿼리 실행 실패") from e

class GoogleSheetConnector:
    def __init__(self, credentials_file, spreadsheet_name):
        self.credentials_file = credentials_file
        self.spreadsheet_name = spreadsheet_name

    def insert_data(self, data, table_name):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, scope)
        gc = gspread.authorize(credentials)
        spreadsheet = gc.open(self.spreadsheet_name)
        sheet_name = table_name
        try:
            self.sheet = spreadsheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            # sheet가 존재하지 않을때 sheet 생성
            self.sheet = spreadsheet.add_worksheet(title=sheet_name, rows=MAX_ROWS, cols=MAX_COLS)
            headers = ["id", "name", "text", "link", "datetime"]
            self.sheet.insert_row(headers, index=1)

            # 1행 고정
            self.sheet.freeze(rows=1)

        #데이터 입력
        self.sheet.append_row(data)

class CheckTextFieldExistence(QObject):
    table_existence_checked = pyqtSignal(bool)

    def __init__(self, mysql_connector, table_name, id_text_field, name_text_field):
        super().__init__()
        self.mysql_connector = mysql_connector
        self.table_name = table_name
        self.id_text_field = id_text_field
        self.name_text_field = name_text_field

    def check_fields_existence(self):
        # 테이블이 존재하는지 확인
        self.mysql_connector.connect()
        try:
            query = f"SHOW TABLES LIKE '{self.table_name}'"
            result = self.mysql_connector.execute_query(query)
            table_exists = bool(result)
            if not table_exists:
                self.table_existence_checked.emit(False)
                return

            id_value = self.id_text_field.text()
            name_value = self.name_text_field.text()

            id_query = f"SELECT COUNT(*) FROM 분류 WHERE name = '{id_value}'"
            id_exists = self.mysql_connector.execute_query(id_query)[0][0] > 0

            name_query = f"SELECT COUNT(*) FROM 작업자 WHERE name = '{name_value}'"
            name_exists = self.mysql_connector.execute_query(name_query)[0][0] > 0

            self.table_existence_checked.emit(id_exists and name_exists)
        finally:
            self.mysql_connector.disconnect()

class Input_Button_Clicked(CustomButtonWithStyle):
    def __init__(self, main_window, autocompletion_input_field, id_text_field, name_text_field, longtext_text_field, link_text_field, parent=None):
        super(Input_Button_Clicked, self).__init__("Insert Data", parent)
        self.main_window = main_window
        self.autocompletion_input_field = autocompletion_input_field
        self.id_text_field = id_text_field
        self.name_text_field = name_text_field
        self.longtext_text_field = longtext_text_field
        self.link_text_field = link_text_field
        self.clicked.connect(self.check_table_existence)

    def check_table_existence(self):
        self.table_name = self.autocompletion_input_field.text()
        checker = CheckTextFieldExistence(self.main_window.mysql_connector, self.table_name, self.id_text_field, self.name_text_field)
        checker.table_existence_checked.connect(self.handle_table_existence_checked)
        checker.check_fields_existence()

    def handle_table_existence_checked(self, table_exists):
        if not table_exists:
            QMessageBox.warning(self.main_window, "Table Not Found", "테이블이 존재하지 않습니다.")
            return

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
        try:
            query = f"""
            INSERT INTO {self.table_name} (id, name, text, link, datetime) 
            VALUES (%s, %s, %s, %s, %s)
            """
            data = (self.id_text, self.name_text_field.text(), self.longtext_text_field.text(), self.link_text_field.text(), datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.main_window.mysql_connector.execute_query(query, data)
        finally:
            # 데이터베이스 연결 닫기
            self.main_window.mysql_connector.disconnect()

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

                table_names = [name[0] for name in table_names]

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
            logging.error("Error: %s", e)

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

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

        main_layout.addWidget(frame_with_bar)

        central_widget = QFrame()
        main_layout.addWidget(central_widget)

        self.setCentralWidget(central_widget)

        central_layout = QHBoxLayout(central_widget)

        # 프레임 전환 버튼 추가
        self.frame_buttons_layout = QVBoxLayout()  # 프레임 전환 버튼을 세로로 정렬하기 위해 QVBoxLayout 사용

        self.frame_buttons = []  # 각 프레임의 프레임 전환 버튼을 저장할 리스트
        button_name = ["Input Data", "Delete Data", "Data", "Data"]
        for i in range(4):
            button = CustomButtonWithStyle(button_name[i])
            button.clicked.connect(partial(self.switch_to_frame, i))
            self.frame_buttons_layout.addWidget(button)
            self.frame_buttons.append(button)  # 프레임 전환 버튼을 리스트에 추가

        central_layout.addLayout(self.frame_buttons_layout)

        # 스택 위젯 생성
        self.stacked_widget = QStackedWidget()
        central_layout.addWidget(self.stacked_widget)

        # 폰트 설정
        font_id = QFontDatabase.addApplicationFont("NotoSansKR-Medium.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 10)

        # 프레임 생성 및 스택 위젯에 추가
        self.frames = []
        for i in range(4):
            frame = FrameWithBar(self)
            frame.setFixedWidth(400)  # 프레임의 가로 크기를 30px 늘림
            grid_layout = QGridLayout()
            frame.content_layout.addLayout(grid_layout)
            autocompletion_input_label = QLabel("Target")
            autocompletion_input_label.setFont(font)
            self.autocompletion_input_field = QLineEdit(self)
            self.autocompletion_input_field.setFont(font)
            self.autocompletion_input_field.setStyleSheet("""
                                        border: 2px solid white;
                                        border-radius: 2px;
                                    """)
            self.autocompletion_input_field.setPlaceholderText("회사명을 입력해주세요")
            grid_layout.addWidget(autocompletion_input_label, 0, 0)  # input label을 왼쪽에 배치
            grid_layout.addWidget(self.autocompletion_input_field, 0, 1)  # input field를 오른쪽에 배치

            self.id_text = QLineEdit()
            self.id_text.setFont(font)
            self.id_text.setStyleSheet("""
                border: 2px solid white;
                border-radius: 2px;
            """)
            self.name_text = QLineEdit()
            self.name_text.setFont(font)
            self.name_text.setStyleSheet("""
                border: 2px solid white;
                border-radius: 2px;
            """)
            self.longtext_text = QLineEdit()
            self.longtext_text.setFont(font)
            self.longtext_text.setStyleSheet("""
                border: 2px solid white;
                border-radius: 2px;
            """)
            self.link_text = QLineEdit()
            self.link_text.setFont(font)
            self.link_text.setStyleSheet("""
                border: 2px solid white;
                border-radius: 2px;
            """)

            inputs = {
                "분류": self.id_text,
                "작업자": self.name_text,
                "내용": self.longtext_text,
                "Link": self.link_text
            }

            for g, (label_text, input_widget) in enumerate(inputs.items(), start=1):
                label = QLabel(label_text)
                label.setFont(font)
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

            if i == 3:  # 프레임 4일 때만 버튼 2개 추가
                for k in range(2):
                    button = CustomButtonWithStyle(f"Button {k+1}")
                    button_layout.addWidget(button)
            else:  # 나머지 프레임에는 버튼 1개 추가
                if i == 0:
                    button = Input_Button_Clicked(self, self.autocompletion_input_field, self.id_text, self.name_text,
                                            self.longtext_text, self.link_text)
                    button.setText("Input Data")
                    button_layout.addWidget(button)
                else:
                    button = CustomButtonWithStyle(f"Button 1")
                    button_layout.addWidget(button)

        # 배경색 지정
        central_widget.setStyleSheet("background-color: #292929; color: white;")

        # 현재 보이는 프레임의 버튼은 보이지만 누를 수 없도록 설정
        self.stacked_widget.currentChanged.connect(self.update_buttons_state)
        self.update_buttons_state(self.stacked_widget.currentIndex())

        self.setLayout(main_layout)

        # Google Sheet 연결 정보
        self.google_sheet_connector = GoogleSheetConnector(CREDENTIALS_FILE, SPREADSHEET_NAME)

        # MySQL 연결 정보
        self.mysql_connector = MySQLConnector(DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE)

        # AutocompletionThread 초기화 및 시작
        self.autocompletion_thread = AutocompletionThread(self.mysql_connector)
        self.autocompletion_thread.result.connect(self.update_completer)
        self.autocompletion_thread.start()

    def update_completer(self, autocompletion_data):
        input_fields = self.frames[0].findChildren(QLineEdit)
        for index, data in enumerate(autocompletion_data):
            completer = QCompleter(data, self)
            input_field = input_fields[index]
            input_field.setCompleter(completer)

    def switch_to_frame(self, index):
        if str(index).isdigit():
            self.stacked_widget.setCurrentIndex(int(index))

    def update_buttons_state(self, index):
        # 프레임 전환 버튼 비활성화
        for button in self.frame_buttons:
            button.setEnabled(True)
        if index < len(self.frame_buttons):
            self.frame_buttons[index].setEnabled(False)

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
