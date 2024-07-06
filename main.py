import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QWidget
from PyQt5.QtCore import Qt

# Import custom pages
from login import LoginPage
from signup import SignupPage
from qrcode_gui import QRCodeGenerator
from imageToText import ImageToTextConverter
from fileConverter import FileConverter
from digitalKeyGenerator import DigitalKeyGenerator
from emailTemplateGenerator import EmailTemplateGenerator

class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Home Page')
        self.setGeometry(100, 100, 1000, 600)

        layout = QVBoxLayout()

        # Navbar layout
        navbar_layout = QHBoxLayout()
        navbar_layout.setAlignment(Qt.AlignTop)

        btn_home = QPushButton('Home', self)
        self.style_navbar_button(btn_home)
        navbar_layout.addWidget(btn_home)

        btn_about = QPushButton('About', self)
        self.style_navbar_button(btn_about)
        navbar_layout.addWidget(btn_about)

        layout.addLayout(navbar_layout)

        # Main content layout
        main_content_layout = QVBoxLayout()
        main_content_layout.setAlignment(Qt.AlignCenter)

        # Welcome message
        welcome_label = QLabel('Welcome to MyApp', self)
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet('font-size: 32px; font-weight: bold;')
        main_content_layout.addWidget(welcome_label)

        # Service buttons
        service_layout = QHBoxLayout()
        service_layout.setAlignment(Qt.AlignCenter)

        btn_qr_code = QPushButton('QR Code Generator', self)
        btn_qr_code.clicked.connect(self.showQRCodeGenerator)
        self.style_service_button(btn_qr_code)
        service_layout.addWidget(btn_qr_code)

        btn_image_to_text = QPushButton('Image to Text Converter', self)
        btn_image_to_text.clicked.connect(self.showImageToTextConverter)
        self.style_service_button(btn_image_to_text)
        service_layout.addWidget(btn_image_to_text)

        btn_file_converter = QPushButton('File Converter', self)
        btn_file_converter.clicked.connect(self.showFileConverter)
        self.style_service_button(btn_file_converter)
        service_layout.addWidget(btn_file_converter)

        btn_digital_key = QPushButton('Digital Key Generator', self)
        btn_digital_key.clicked.connect(self.showDigitalKeyGenerator)
        self.style_service_button(btn_digital_key)
        service_layout.addWidget(btn_digital_key)

        btn_email_template = QPushButton('Email Template Generator', self)
        btn_email_template.clicked.connect(self.showEmailTemplateGenerator)
        self.style_service_button(btn_email_template)
        service_layout.addWidget(btn_email_template)

        main_content_layout.addLayout(service_layout)
        layout.addLayout(main_content_layout)

        self.setLayout(layout)
        self.setStyleSheet('background-color: #f0f0f0;')  # Background color

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
                padding: 15px 30px;
                margin: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        ''')

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

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Main Application')
        self.setGeometry(100, 100, 1200, 800)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.home_page = HomePage(self)
        self.login_page = LoginPage(self)
        self.signup_page = SignupPage(self)
        self.qr_code_generator_page = QRCodeGenerator(self)
        self.image_to_text_converter_page = ImageToTextConverter(self)
        self.file_converter_page = FileConverter(self)
        self.digital_key_generator_page = DigitalKeyGenerator(self)
        self.email_template_generator_page = EmailTemplateGenerator(self)

        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.signup_page)
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.qr_code_generator_page)
        self.stacked_widget.addWidget(self.image_to_text_converter_page)
        self.stacked_widget.addWidget(self.file_converter_page)
        self.stacked_widget.addWidget(self.digital_key_generator_page)
        self.stacked_widget.addWidget(self.email_template_generator_page)

        self.stacked_widget.setCurrentWidget(self.login_page)  # Show login page first

    def showMainPage(self):
        self.stacked_widget.setCurrentWidget(self.home_page)

    def showSignupPage(self):
        self.stacked_widget.setCurrentWidget(self.signup_page)

    def showLoginPage(self):
        self.stacked_widget.setCurrentWidget(self.login_page)

    def showQRCodeGenerator(self):
        self.stacked_widget.setCurrentWidget(self.qr_code_generator_page)

    def showImageToTextConverter(self):
        self.stacked_widget.setCurrentWidget(self.image_to_text_converter_page)

    def showFileConverter(self):
        self.stacked_widget.setCurrentWidget(self.file_converter_page)

    def showDigitalKeyGenerator(self):
        self.stacked_widget.setCurrentWidget(self.digital_key_generator_page)

    def showEmailTemplateGenerator(self):
        self.stacked_widget.setCurrentWidget(self.email_template_generator_page)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
