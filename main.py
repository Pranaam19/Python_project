import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QStackedWidget, QWidget, QGridLayout, QLineEdit, QListWidget, QFileDialog
)
from PyQt5.QtCore import Qt
import sqlite3
import os
import qrcode

# Import custom pages
from login import LoginPage
from signup import SignupPage
from qrcode_gui import QRCodeGenerator
from imageToText import ImageToTextConverter
from fileConverter import FileConverter
from digitalKeyGenerator import DigitalKeyGenerator
from emailTemplateGenerator import EmailTemplateGenerator
from watermark import WatermarkGenerator
from watermark_removal import WatermarkRemoval
from TextToSpeech import TextToSpeechConverter

class HistoryAndFilesPage(QWidget):
    def __init__(self, main_app=None, parent=None):
        super().__init__(parent)
        self.main_app = main_app
        self.initUI()

    def initUI(self):
        self.setWindowTitle('History and Files')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.label = QLabel('History and Files', self)
        layout.addWidget(self.label)

        self.file_list = QListWidget(self)
        layout.addWidget(self.file_list)

        self.setLayout(layout)
        self.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
                color: black;
            }
            QListWidget {
                font-size: 14px;
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        """)

    def load_files(self):
        self.file_list.clear()
        user_id = self.main_app.user_id
        cursor = self.main_app.conn.cursor()
        cursor.execute("SELECT file_name, file_path FROM generated_files WHERE user_id=?", (user_id,))
        files = cursor.fetchall()
        for file in files:
            self.file_list.addItem(f"{file[0]} - {file[1]}")


class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Home Page')
        self.setGeometry(100, 100, 1200, 800)

        main_layout = QVBoxLayout()

        # Navbar
        navbar_layout = QHBoxLayout()
        navbar_layout.setAlignment(Qt.AlignTop)

        logo_label = QLabel('MyApp', self)
        logo_label.setStyleSheet('font-size: 24px; font-weight: bold; color: #ffffff;')
        navbar_layout.addWidget(logo_label)

        search_bar = QLineEdit(self)
        search_bar.setPlaceholderText('Search services...')
        search_bar.setStyleSheet('padding: 10px; border-radius: 5px;')
        navbar_layout.addWidget(search_bar)

        search_button = QPushButton('Search', self)
        search_button.setStyleSheet('background-color: #ff9900; color: white; padding: 10px 20px; border-radius: 5px;')
        navbar_layout.addWidget(search_button)

        btn_login = QPushButton('Login', self)
        btn_login.clicked.connect(self.showLoginPage)
        self.style_navbar_button(btn_login)
        navbar_layout.addWidget(btn_login)

        btn_signup = QPushButton('Sign Up', self)
        btn_signup.clicked.connect(self.showSignupPage)
        self.style_navbar_button(btn_signup)
        navbar_layout.addWidget(btn_signup)

        navbar_container = QWidget()
        navbar_container.setLayout(navbar_layout)
        navbar_container.setStyleSheet('background-color: #232f3e; padding: 10px;')
        main_layout.addWidget(navbar_container)

        # Categories section
        categories_layout = QHBoxLayout()
        categories_layout.setAlignment(Qt.AlignCenter)

        categories = ['QR Code', 'Image to Text', 'File Converter', 'Digital Key', 'Email Template', 'Watermark', 'Watermark Removal']
        for category in categories:
            category_button = QPushButton(category, self)
            category_button.setStyleSheet('''
                QPushButton {
                    background-color: #0078d7;
                    color: white;
                    font-size: 18px;
                    padding: 15px 30px;
                    margin: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #005a9e;
                }
            ''')
            category_button.clicked.connect(lambda checked, c=category: self.showCategoryPage(c))
            categories_layout.addWidget(category_button)

        main_layout.addLayout(categories_layout)

        # Main content
        main_content_layout = QGridLayout()
        main_content_layout.setAlignment(Qt.AlignTop)

        services = [
            ('QR Code Generator', self.showQRCodeGenerator),
            ('Image to Text Converter', self.showImageToTextConverter),
            ('File Converter', self.showFileConverter),
            ('Digital Key Generator', self.showDigitalKeyGenerator),
            ('Email Template Generator', self.showEmailTemplateGenerator),
            ('Watermark Generator', self.showWatermarkGenerator),
            ('Watermark Removal', self.showWatermarkRemoval),
            ('Text to Speech', self.showTextToSpeechConverter),
            ('History and Files', self.showHistoryAndFilesPage)
        ]

        for idx, (service_name, service_func) in enumerate(services):
            service_button = QPushButton(service_name, self)
            service_button.clicked.connect(service_func)
            self.style_service_button(service_button)
            main_content_layout.addWidget(service_button, idx // 2, idx % 2)

        main_layout.addLayout(main_content_layout)

        self.setLayout(main_layout)
        self.setStyleSheet('background-color: #f0f0f0;')

    def style_navbar_button(self, button):
        button.setStyleSheet('''
            QPushButton {
                background-color: #0078d7;
                color: white;
                font-size: 18px;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        ''')

    def style_service_button(self, button):
        button.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                padding: 20px 40px;
                margin: 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        ''')

    def showCategoryPage(self, category):
        QMessageBox.information(self, 'Category Selected', f'You selected: {category}')

    def showQRCodeGenerator(self):
        self.parent().parent().showQRCodeGenerator()

    def showImageToTextConverter(self):
        self.parent().parent().showImageToTextConverter()

    def showFileConverter(self):
        self.parent().parent().showFileConverter()

    def showDigitalKeyGenerator(self):
        self.parent().parent().showDigitalKeyGenerator()

    def showEmailTemplateGenerator(self):
        self.parent().parent().showEmailTemplateGenerator()

    def showWatermarkGenerator(self):
        self.parent().parent().showWatermarkGenerator()

    def showWatermarkRemoval(self):
        self.parent().parent().showWatermarkRemoval()

    def showTextToSpeechConverter(self):
        self.parent().parent().showTextToSpeechConverter()

    def showLoginPage(self):
        self.parent().parent().showLoginPage()

    def showSignupPage(self):
        self.parent().parent().showSignupPage()

    def showHistoryAndFilesPage(self):
        self.parent().parent().showHistoryAndFilesPage()


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect('app_data.db')
        self.create_tables()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Main Application')
        self.setGeometry(100, 100, 1200, 800)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.user_id = None

        self.login_page = LoginPage(self)
        self.signup_page = SignupPage(self)
        self.home_page = HomePage(self)
        self.qr_code_generator = QRCodeGenerator(self)
        self.image_to_text_converter = ImageToTextConverter(self)
        self.file_converter = FileConverter(self)
        self.digital_key_generator = DigitalKeyGenerator(self)
        self.email_template_generator = EmailTemplateGenerator(self)
        self.watermark_generator = WatermarkGenerator(self)
        self.watermark_removal = WatermarkRemoval(self)
        self.text_to_speech_converter = TextToSpeechConverter(self)
        self.history_and_files_page = HistoryAndFilesPage(self)

        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.signup_page)
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.qr_code_generator)
        self.stacked_widget.addWidget(self.image_to_text_converter)
        self.stacked_widget.addWidget(self.file_converter)
        self.stacked_widget.addWidget(self.digital_key_generator)
        self.stacked_widget.addWidget(self.email_template_generator)
        self.stacked_widget.addWidget(self.watermark_generator)
        self.stacked_widget.addWidget(self.watermark_removal)
        self.stacked_widget.addWidget(self.text_to_speech_converter)
        self.stacked_widget.addWidget(self.history_and_files_page)

        self.showLoginPage()

    def showLoginPage(self):
        self.stacked_widget.setCurrentWidget(self.login_page)

    def showSignupPage(self):
        self.stacked_widget.setCurrentWidget(self.signup_page)

    def showMainPage(self):
        self.stacked_widget.setCurrentWidget(self.home_page)

    def showQRCodeGenerator(self):
        self.stacked_widget.setCurrentWidget(self.qr_code_generator)

    def showImageToTextConverter(self):
        self.stacked_widget.setCurrentWidget(self.image_to_text_converter)

    def showFileConverter(self):
        self.stacked_widget.setCurrentWidget(self.file_converter)

    def showDigitalKeyGenerator(self):
        self.stacked_widget.setCurrentWidget(self.digital_key_generator)

    def showEmailTemplateGenerator(self):
        self.stacked_widget.setCurrentWidget(self.email_template_generator)

    def showWatermarkGenerator(self):
        self.stacked_widget.setCurrentWidget(self.watermark_generator)

    def showWatermarkRemoval(self):
        self.stacked_widget.setCurrentWidget(self.watermark_removal)

    def showTextToSpeechConverter(self):
        self.stacked_widget.setCurrentWidget(self.text_to_speech_converter)

    def showHistoryAndFilesPage(self):
        self.history_and_files_page.load_files()
        self.stacked_widget.setCurrentWidget(self.history_and_files_page)

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS generated_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                file_name TEXT,
                file_path TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.conn.commit()

    def store_generated_file(self, user_id, file_name, file_path):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO generated_files (user_id, file_name, file_path)
            VALUES (?, ?, ?)
        ''', (user_id, file_name, file_path))
        self.conn.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
