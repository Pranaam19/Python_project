import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from login import LoginPage
from signup import SignupPage
from imageToText import ImageToTextConverter
from qrcode_gui import QRCodeGenerator
from fileConverter import FileConverter
from digitalKeyGenerator import DigitalKeyGenerator
import sqlite3

def create_users_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)')
    conn.commit()
    conn.close()

class MainPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Main Page')
        self.setGeometry(100, 100, 1000, 600)

        self.layout = QVBoxLayout()

        navbar_layout = QHBoxLayout()
        navbar_layout.setAlignment(Qt.AlignTop)

        btn_home = QPushButton('Home', self)
        btn_home.clicked.connect(self.showHome)
        self.style_navbar_button(btn_home)
        navbar_layout.addWidget(btn_home)

        btn_about = QPushButton('About', self)
        btn_about.clicked.connect(self.showAbout)
        self.style_navbar_button(btn_about)
        navbar_layout.addWidget(btn_about)

        self.layout.addLayout(navbar_layout)

        main_content_layout = QHBoxLayout()

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setAlignment(Qt.AlignTop)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)

        sidebar_widget = QWidget()
        sidebar_widget.setStyleSheet('background-color: #333; color: white;')
        sidebar_layout.addWidget(sidebar_widget)

        welcome_label = QLabel('Welcome to MyApp', self)
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet('font-size: 24px; font-weight: bold; padding: 20px;')
        sidebar_layout.addWidget(welcome_label)

        main_content_layout.addLayout(sidebar_layout)

        service_layout = QVBoxLayout()
        service_layout.setAlignment(Qt.AlignTop)

        btn_qr_code = QPushButton('QR Code Generator', self)
        btn_qr_code.clicked.connect(self.showQRCodeGenerator)
        self.style_button(btn_qr_code)
        service_layout.addWidget(btn_qr_code)

        btn_image_to_text = QPushButton('Image to Text Converter', self)
        btn_image_to_text.clicked.connect(self.showImageToTextConverter)
        self.style_button(btn_image_to_text)
        service_layout.addWidget(btn_image_to_text)

        btn_file_converter = QPushButton('File Converter', self)
        btn_file_converter.clicked.connect(self.showFileConverter)
        self.style_button(btn_file_converter)
        service_layout.addWidget(btn_file_converter)

        btn_digital_key = QPushButton('Digital Key Generator', self)
        btn_digital_key.clicked.connect(self.showDigitalKeyGenerator)
        self.style_button(btn_digital_key)
        service_layout.addWidget(btn_digital_key)

        main_content_layout.addLayout(service_layout)

        self.layout.addLayout(main_content_layout)
        self.setLayout(self.layout)
        self.setStyleSheet('background-color: #f0f0f0;')

        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.addWidget(QWidget())
        self.stacked_widget.addWidget(QRCodeGenerator())
        self.stacked_widget.addWidget(ImageToTextConverter())
        self.stacked_widget.addWidget(FileConverter())
        self.stacked_widget.addWidget(DigitalKeyGenerator())

        main_content_layout.addWidget(self.stacked_widget)

    def style_navbar_button(self, button):
        button.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        ''')

    def style_button(self, button):
        button.setStyleSheet('''
            QPushButton {
                background-color: #008CBA;
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #007BB5;
            }
        ''')

    def showQRCodeGenerator(self):
        self.stacked_widget.setCurrentIndex(1)

    def showImageToTextConverter(self):
        self.stacked_widget.setCurrentIndex(2)

    def showFileConverter(self):
        self.stacked_widget.setCurrentIndex(3)

    def showDigitalKeyGenerator(self):
        self.stacked_widget.setCurrentIndex(4)

    def showHome(self):
        self.stacked_widget.setCurrentIndex(0)

    def showAbout(self):
        QMessageBox.information(self, "About", "This is an example application.")

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Application')
        self.setGeometry(100, 100, 1000, 600)

        self.login_page = LoginPage(self)
        self.signup_page = SignupPage(self)
        self.main_page = MainPage(self)

        self.addWidget(self.login_page)
        self.addWidget(self.signup_page)
        self.addWidget(self.main_page)

        self.setCurrentWidget(self.login_page)

    def showSignupPage(self):
        self.setCurrentWidget(self.signup_page)

    def showLoginPage(self):
        self.setCurrentWidget(self.login_page)

    def showMainPage(self):
        self.setCurrentWidget(self.main_page)

if __name__ == '__main__':
    create_users_table()
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
