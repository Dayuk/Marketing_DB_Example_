import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QLabel, QLineEdit, \
    QStackedWidget, QGridLayout, QWidget


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


class FrameWithBar(QFrame):
    def __init__(self, main_window, parent=None):
        super(FrameWithBar, self).__init__(parent)

        self.main_window = main_window

        self.title_bar = QWidget()
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.addStretch(2)

        minimize_button = CustomButton("–", self)
        minimize_button.setFixedSize(30, 30)
        minimize_button.clicked.connect(self.main_window.showMinimized)
        minimize_button.setFont(QFont("NotoSansKR-Medium", 10, QFont.Bold))
        title_layout.addWidget(minimize_button)

        close_button = CustomButton("X", self)
        close_button.setFixedSize(30, 30)
        close_button.clicked.connect(self.main_window.close)
        close_button.setFont(QFont("NotoSansKR-Medium", 10, QFont.Bold))
        title_layout.addWidget(close_button)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.title_bar)

        self.content_layout = QVBoxLayout()
        self.layout.addLayout(self.content_layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setWindowTitle("프레임 전환 UI")

        main_layout = QVBoxLayout()

        central_widget = QFrame()
        main_layout.addWidget(central_widget)

        self.setCentralWidget(central_widget)

        central_layout = QHBoxLayout(central_widget)

        # 프레임 전환 버튼 추가
        self.frame_buttons_layout = QVBoxLayout()  # 프레임 전환 버튼을 세로로 정렬하기 위해 QVBoxLayout 사용

        self.frame_buttons = []  # 각 프레임의 프레임 전환 버튼을 저장할 리스트

        for i in range(4):
            button = CustomButton(f"프레임 {i+1}로 전환")
            button.clicked.connect(lambda state, x=i: self.switch_to_frame(x))
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
            frame = QFrame()
            grid_layout = QGridLayout()
            frame_layout = QVBoxLayout(frame)
            frame_layout.addWidget(FrameWithBar(self))
            frame_layout.setAlignment(Qt.AlignTop)
            frame_layout.addLayout(grid_layout)

            for j in range(4):
                input_label = QLabel(f"Input {j+1}:")
                input_label.setFont(font)
                input_field = QLineEdit()
                grid_layout.addWidget(input_label, j, 0)  # input label을 왼쪽에 배치
                grid_layout.addWidget(input_field, j, 1)  # input field를 오른쪽에 배치

            self.stacked_widget.addWidget(frame)
            self.frames.append(frame)

            # 프레임에 버튼 추가
            button_layout = QHBoxLayout()  # 버튼을 가로로 정렬하기 위해 QHBoxLayout 사용
            frame_layout.addLayout(button_layout)

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
        self.stacked_widget.setCurrentIndex(index)

    def update_buttons_state(self, index):
        # 프레임 전환 버튼 비활성화
        for button in self.frame_buttons:
            button.setEnabled(True)
        self.frame_buttons[index].setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
