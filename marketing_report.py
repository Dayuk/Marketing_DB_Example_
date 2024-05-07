import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt, QPoint, QThread, pyqtSignal
import pymysql
from functools import partial
import time
from datetime import datetime

class CustomButton(QPushButton):
    def __init__(self, text, parent=None):
        super(CustomButton, self).__init__(text, parent)

        # 폰트 설정
        font_id = QFontDatabase.addApplicationFont("NotoSansKR-Medium.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 16)
        self.setFont(font)

        # 버튼 스타일 설정
        self.setStyleSheet("""
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
        """)

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
            print("MySQL 데이터베이스에 연결되었습니다.")
        except Exception as e:
            print("MySQL 데이터베이스 연결 오류:", e)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("MySQL 데이터베이스 연결이 닫혔습니다.")

    def execute_query(self, query):
        try:
            if self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute(query)
                    self.connection.commit()
                    print("쿼리가 성공적으로 실행되었습니다.")
        except Exception as e:
            self.connection.rollback()
            print("쿼리 실행 오류:", e)

class Button1Clicked(CustomButton):
    def __init__(self, main_window, autocompletion_input_field, id_text_field, name_text_field, longtext_text_field, link_text_field, parent=None):
        super(Button1Clicked, self).__init__("Insert Data", parent)
        self.main_window = main_window
        self.autocompletion_input_field = autocompletion_input_field
        self.id_text_field = id_text_field
        self.name_text_field = name_text_field
        self.longtext_text_field = longtext_text_field
        self.link_text_field = link_text_field
        self.clicked.connect(self.insert_data)

    def insert_data(self):
        print("1")
        current_frame_index = self.main_window.stacked_widget.currentIndex()
        current_frame = self.main_window.frames[current_frame_index]

        # 데이터베이스에 연결
        self.main_window.mysql_connector.connect()

        # 데이터 삽입
        table_name = self.autocompletion_input_field.text()
        id_text = self.id_text_field.text()
        name_text = self.name_text_field.text()
        text_text = self.longtext_text_field.text()
        link_text = self.link_text_field.text()
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = f"INSERT INTO {table_name} (id, `index`, name, text, link, datetime) VALUES ('{id_text}', 1, '{name_text}', '{text_text}', '{link_text}', '{current_datetime}')"
        self.main_window.mysql_connector.execute_query(query)

        # 데이터베이스 연결 닫기
        self.main_window.mysql_connector.disconnect()

        # 성공 메시지 표시
        QMessageBox.information(self.main_window, "Success", "데이터가 성공적으로 삽입되었습니다.")


class MySQLInputDataThread(QThread):
    def __init__(self, button_clicked_object):
        super(MySQLInputDataThread, self).__init__()
        self.button_clicked_object = button_clicked_object

    def run(self):
        self.button_clicked_object.start()  # QThread의 start 메서드 호출

class AutocompletionThread(QThread):
    result = pyqtSignal(list)

    def __init__(self, mysql_connector):
        super(AutocompletionThread, self).__init__()
        self.mysql_connector = mysql_connector

    def run(self):
        try:
            while True:
                # MySQL Connection
                self.mysql_connector.connect()

                # Cursor to execute queries
                cursor = self.mysql_connector.connection.cursor()

                # Query to get table names
                cursor.execute("SHOW TABLES")

                # Fetch all table names
                table_names = cursor.fetchall()

                # Extract table names
                table_names = [name[0] for name in table_names]
                self.result.emit(table_names)

                # Close Cursor and Connection
                cursor.close()
                self.mysql_connector.disconnect()

                # Sleep for 30 seconds
                time.sleep(30)

        except Exception as e:
            print("Error:", e)

class FrameWithBarStyle:
    @staticmethod
    def get_style_sheet():
        return """
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

class FrameWithBar(QFrame):
    def __init__(self, main_window, parent=None):
        super(FrameWithBar, self).__init__(parent)

        self.main_window = main_window

        self.title_bar = QWidget()
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.addStretch(2)

        # Minimize Button
        minimize_button = QPushButton("–", self)
        minimize_button.setObjectName("MinimizeButton")
        minimize_button.setFixedSize(25, 25)
        minimize_button.clicked.connect(self.main_window.showMinimized)
        title_layout.addWidget(minimize_button)

        # Close Button
        close_button = QPushButton("X", self)
        close_button.setObjectName("CloseButton")
        close_button.setFixedSize(25, 25)
        close_button.clicked.connect(self.main_window.close)
        title_layout.addWidget(close_button)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.title_bar)

        self.content_layout = QVBoxLayout()
        self.layout.addLayout(self.content_layout)

        self.setStyleSheet(FrameWithBarStyle.get_style_sheet())

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

        self.setWindowTitle("프레임 전환 UI")

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
            button = CustomButton(button_name[i])
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
        self.colums = ["종류", "작업자", "내용", "링크"]
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
                    button = CustomButton(f"Button {k+1}")
                    button_layout.addWidget(button)
            else:  # 나머지 프레임에는 버튼 1개 추가
                if i == 0:
                    button = Button1Clicked(self, self.autocompletion_input_field, self.id_text, self.name_text,
                                            self.longtext_text, self.link_text)
                    button.setText("Input Data")
                    button_layout.addWidget(button)
                else:
                    button = CustomButton(f"Button 1")
                    button_layout.addWidget(button)

        # 배경색 지정
        central_widget.setStyleSheet("background-color: #292929; color: white;")

        # 현재 보이는 프레임의 버튼은 보이지만 누를 수 없도록 설정
        self.stacked_widget.currentChanged.connect(self.update_buttons_state)
        self.update_buttons_state(self.stacked_widget.currentIndex())

        self.setLayout(main_layout)

        # MySQL 연결 정보
        host = "127.0.0.1"
        user = "Program_User"
        password = "rlaqjatn256^"
        database = "my_database"

        # MySQLConnector 인스턴스 생성
        self.mysql_connector = MySQLConnector(host, user, password, database)

        # AutocompletionThread 초기화 및 시작
        self.autocompletion_thread = AutocompletionThread(self.mysql_connector)
        self.autocompletion_thread.result.connect(self.update_completer)
        self.autocompletion_thread.start()

    def mysql_input_data(self):
        mysql_input_data_thread = MySQLInputDataThread(Button1Clicked(self, self.autocompletion_input_field, self.id_text, self.name_text, self.longtext_text, self.link_text))
        mysql_input_data_thread.start()

    def update_completer(self, table_names):
        completer = QCompleter(table_names, self)
        for frame in self.frames:
            autocompletion_input_field = frame.findChild(QLineEdit)
            autocompletion_input_field.setCompleter(completer)

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
