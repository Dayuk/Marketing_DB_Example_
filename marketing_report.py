import sys
from functools import partial

import pymysql
from PyQt5.QtCore import Qt, QPoint  # QPoint import 추가
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtWidgets import *


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
            autocompletion_input_field = QLineEdit()
            autocompletion_input_field.setFont(font)
            autocompletion_input_field.setStyleSheet("""
                                        border: 2px solid white;
                                        border-radius: 2px;
                                    """)
            autocompletion_input_field.setPlaceholderText("회사명을 입력해주세요")
            # 자동완성 기능 추가
            self.add_autocompletion_to_input_field(autocompletion_input_field)
            grid_layout.addWidget(autocompletion_input_label, 0, 0)  # input label을 왼쪽에 배치
            grid_layout.addWidget(autocompletion_input_field, 0, 1)  # input field를 오른쪽에 배치

            for j in range(4):
                input_label = QLabel(self.colums[j])
                input_label.setFont(font)
                input_field = QLineEdit()
                input_field.setStyleSheet("""
                                            border: 2px solid white;
                                            border-radius: 2px;
                                        """)
                grid_layout.addWidget(input_label, j+1, 0)  # input label을 왼쪽에 배치
                grid_layout.addWidget(input_field, j+1, 1)  # input field를 오른쪽에 배치

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
                button = CustomButton(f"Button 1")
                button_layout.addWidget(button)

        # 배경색 지정
        central_widget.setStyleSheet("background-color: #292929; color: white;")

        # 현재 보이는 프레임의 버튼은 보이지만 누를 수 없도록 설정
        self.stacked_widget.currentChanged.connect(self.update_buttons_state)
        self.update_buttons_state(self.stacked_widget.currentIndex())

        self.setLayout(main_layout)

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

    def add_autocompletion_to_input_field(self, input_field):
        try:
            # MySQL Connection
            connection = pymysql.connect(
                host="127.0.0.1",
                user="Program_User",
                password="rlaqjatn256^",
                database="my_database"
            )

            # Cursor to execute queries
            cursor = connection.cursor()

            # Query to get table names
            cursor.execute("SHOW TABLES")

            # Fetch all table names
            table_names = cursor.fetchall()

            # Extract table names
            table_names = [name[0] for name in table_names]

            # Set AutoCompletion
            completer = QCompleter(table_names)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            input_field.setCompleter(completer)

            # Close Cursor and Connection
            cursor.close()
            connection.close()

        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
