import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QTextBrowser, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import pytesseract
from PIL import Image

# Import the ImageToTextConverter page
from imageToText import ImageToTextConverter
from qrcode_gui import QRCodeGenerator  # Example import

class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Main Page')
        self.setGeometry(100, 100, 1000, 600)  # Larger size suitable for a tablet

        self.layout = QVBoxLayout()

        # Top Navbar layout
        navbar_layout = QHBoxLayout()
        navbar_layout.setAlignment(Qt.AlignTop)  # Align to the top

        # Navbar buttons
        btn_home = QPushButton('Home', self)
        self.style_navbar_button(btn_home)
        navbar_layout.addWidget(btn_home)

        btn_about = QPushButton('About', self)
        self.style_navbar_button(btn_about)
        navbar_layout.addWidget(btn_about)

        self.layout.addLayout(navbar_layout)

        # Main content layout (sidebar and service buttons)
        main_content_layout = QHBoxLayout()

        # Sidebar layout
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setAlignment(Qt.AlignTop)  # Align to the top
        sidebar_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        # Sidebar background color and welcome text
        sidebar_widget = QWidget()
        sidebar_widget.setStyleSheet('background-color: #333; color: white;')
        sidebar_layout.addWidget(sidebar_widget)

        # Welcome text
        welcome_label = QLabel('Welcome to MyApp', self)
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet('font-size: 24px; font-weight: bold; padding: 20px;')
        sidebar_layout.addWidget(welcome_label)

        main_content_layout.addLayout(sidebar_layout)

        # Service layout
        service_layout = QVBoxLayout()
        service_layout.setAlignment(Qt.AlignTop)  # Align to the top

        btn_qr_code = QPushButton('QR Code Generator', self)
        btn_qr_code.clicked.connect(self.showQRCodeGenerator)
        self.style_button(btn_qr_code)  # Apply custom button styling
        service_layout.addWidget(btn_qr_code)

        btn_image_to_text = QPushButton('Image to Text Converter', self)
        btn_image_to_text.clicked.connect(self.showImageToTextConverter)  # Connect to image-to-text converter
        self.style_button(btn_image_to_text)  # Apply custom button styling
        service_layout.addWidget(btn_image_to_text)

        main_content_layout.addLayout(service_layout)

        self.layout.addLayout(main_content_layout)

        self.setLayout(self.layout)

        # Apply background color to the main page
        self.setStyleSheet('background-color: #f0f0f0;')

    def style_navbar_button(self, button):
        button.setStyleSheet('''
            QPushButton {
                background-color: #008CBA; /* Blue */
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 10px;
                width: 120px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005F6B; /* Darker blue */
            }
        ''')

    def style_button(self, button):
        button.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50; /* Green */
                border: none;
                color: white;
                padding: 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 18px;
                margin: 20px;
                width: 300px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45a049; /* Darker green */
            }
        ''')

    def showQRCodeGenerator(self):
        self.qr_window = QRCodeGenerator()
        self.qr_window.show()

    def showImageToTextConverter(self):
        self.image_to_text_window = ImageToTextConverter()
        self.image_to_text_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_page = MainPage()
    main_page.show()
    sys.exit(app.exec_())
