
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QTableWidget, QComboBox, QTableWidgetItem, QMessageBox, QCompleter, QTabWidget
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QStringListModel, Qt
from settings import FONT_PATH

class FontManager:
    def __init__(self, font_file=FONT_PATH, font_size=12):
        self.font_file = font_file
        self.font_size = self.adjust_font_size(font_size)
        self.font_id = QFontDatabase.addApplicationFont(self.font_file)
        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]

    def get_font(self):
        return QFont(self.font_family, self.font_size)

    def adjust_font_size(self, base_size):
        screen = QApplication.primaryScreen()
        resolution = screen.size()
        height = resolution.height()
        
        # 해상도에 따른 폰트 크기 조정
        if height < 800:
            return base_size - 4  # 낮은 해상도
        elif height <= 1080:
            return base_size
        elif height <= 1440:
            return base_size + 6
        elif height <= 2160:
            return base_size + 12
        return base_size

class CustomButtonWithStyle(QPushButton):
    def __init__(self, text, parent=None):
        super(CustomButtonWithStyle, self).__init__(text, parent)
        self.init_ui()

    def init_ui(self):
        # 폰트 설정
        font_manager = FontManager(font_size=11)
        self.setFont(font_manager.get_font())

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

class StyledLineEdit(QLineEdit):
    def __init__(self, parent=None, placeholderText=None, echoMode=None):
        super(StyledLineEdit, self).__init__(parent)
        
        # 폰트 설정
        font_manager = FontManager(font_size=12)
        self.setFont(font_manager.get_font())
        
        # 스타일 설정
        self.setStyleSheet("""
            border: 2px solid white;
            border-radius: 2px;
        """)
        
        if placeholderText:
            self.setPlaceholderText(placeholderText)

        if echoMode:
            self.setEchoMode(echoMode)

class StyledLabel(QLabel):
    def __init__(self, text, parent=None):
        super(StyledLabel, self).__init__(text, parent)
        self.init_ui()

    def init_ui(self):
        # 폰트 설정
        font_manager = FontManager(font_size=11)
        self.setFont(font_manager.get_font())

        # 스타일 설정
        self.setStyleSheet("""
        """)

class StyledTableWidget(QTableWidget):
    def __init__(self, rows=0, columns=0, parent=None):
        super(StyledTableWidget, self).__init__(rows, columns, parent)
        self.init_ui()

    def init_ui(self):
        # 폰트 설정
        font_manager = FontManager(font_size=10)
        self.setFont(font_manager.get_font())

        self.horizontalHeader().setFont(font_manager.get_font())  # 수평 헤더에 폰트 설정
        self.verticalHeader().setFont(font_manager.get_font())  # 수직 헤더에 폰트 적용
        font_size = font_manager.get_font().pointSize()
        header_height = font_size + 20  # 폰트 크기에 따라 헤더 높이 조정
        self.horizontalHeader().setFixedHeight(header_height)  # 수평 헤더의 높이 설정

        # 가로 스크롤바 비활성화
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 스타일 설정
        self.setStyleSheet("""
            QTableWidget {
                background-color: #292929;
                border: 1px solid #ffffff;
            }
            QTableWidget::item {
                background-color: #292929;
                color: white;
            }
            QTableWidget::item:selected {
                background-color: #ffffff;
                color: black;
            }
            QHeaderView::section {
                background-color: #292929;
                color: #ffffff;
                border: 1px solid #ffffff;
                padding: 5px;
            }
            QHeaderView::section:horizontal {
                background-color: #292929;
                color: white;
            }
            QTableCornerButton::section {
                background-color: #292929;
                border: 1px solid #ffffff;
            }
        """)

        # 셀 아이템에 폰트 적용
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                item = self.item(row, col)
                if item is not None:
                    item.setFont(font_manager.get_font())
                else:
                    # 새 아이템 생성 및 폰트 설정
                    new_item = QTableWidgetItem("Example Text")
                    new_item.setFont(font_manager.get_font())
                    self.setItem(row, col, new_item)

        # 열 너비 자동 조정
        self.resizeColumnsToContents()
        self.horizontalHeader().setStretchLastSection(True)

class StyledComboBox(QComboBox):
    def __init__(self, parent=None):
        super(StyledComboBox, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        # 폰트 설정
        font_manager = FontManager(font_size=11)
        self.setFont(font_manager.get_font())

        # 스타일 설정
        self.setStyleSheet("""
            QComboBox {
                background-color: #292929;
                border: 1px solid white;
            }
        """)

class StyledMessageBox(QMessageBox):
    def __init__(self, parent=None, title="", message=""):
        super(StyledMessageBox, self).__init__(parent)
        self.setWindowTitle(title)
        self.setText(message)
        self.init_ui()
        self.add_custom_buttons()
        self.exec_()  # 메시지 박스를 실행

    def init_ui(self):
        # 폰트 설정
        font_manager = FontManager(font_size=12)
        self.setFont(font_manager.get_font())

        # 스타일 설정
        self.setStyleSheet("""
            QMessageBox {
                background-color: #333333;
                color: white;
            }
            QMessageBox QLabel {
                color: white;
            }
        """)

    def add_custom_buttons(self):
        # 기본 버튼 제거
        self.setStandardButtons(QMessageBox.NoButton)

        # 사용자 정의 버튼 추가
        ok_button = CustomButtonWithStyle("OK", self)
        cancel_button = CustomButtonWithStyle("Cancel", self)

        # 버튼 클릭 시그널 연결
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        # 버튼을 메시지 박스에 추가
        self.addButton(ok_button, QMessageBox.AcceptRole)
        self.addButton(cancel_button, QMessageBox.RejectRole)

class StyledCompleter(QCompleter):
    def __init__(self, data, parent=None):
        super(StyledCompleter, self).__init__(parent)
        self.setModel(QStringListModel(data))  # 데이터를 모델로 설정
        self.init_ui()

    def init_ui(self):
        # 폰트 설정
        font_manager = FontManager(font_size=11)  # FontManager 클래스는 폰트를 관리합니다.
        self.popup().setFont(font_manager.get_font())

        # 스타일 시트 설정
        self.popup().setStyleSheet("""
            QListView {
                background-color: #292929;
                color: white;
                border: 1px solid white;
            }
            QListView::item {
                padding: 5px;
            }
            QListView::item:selected {
                background-color: white;
                color: #292929;
            }
        """)

class StyledTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super(StyledTabWidget, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        font_manager = FontManager(font_size=11)
        self.setFont(font_manager.get_font())
        # 스타일 시트 설정
        font_size = font_manager.get_font().pointSize()
        tab_height = font_size + 4

        self.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid #292929;
                background: #292929;
            }}
            QTabBar::tab {{
                background: #292929;
                color: #ffffff;
                padding: 10px;
                border: 1px solid #fff;
                border-radius: 4px;
                height: {tab_height}px;
            }}
            QTabBar::tab:selected, QTabBar::tab:hover {{
                background: #ffffff;
                color: #292929;
                border-color: #292929;
            }}
        """)
