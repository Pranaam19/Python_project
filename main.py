import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox, QStackedWidget
from PyQt5.QtCore import Qt
from imageToText import ImageToTextConverter
from qrcode_gui import QRCodeGenerator
from fileConverter import FileConverter
from digitalKeyGenerator import DigitalKeyGenerator

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
        btn_home.clicked.connect(self.showHome)
        self.style_navbar_button(btn_home)
        navbar_layout.addWidget(btn_home)

        btn_about = QPushButton('About', self)
        btn_about.clicked.connect(self.showAbout)
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

        btn_file_converter = QPushButton('File Converter', self)
        btn_file_converter.clicked.connect(self.showFileConverter)  # Connect to file converter
        self.style_button(btn_file_converter)  # Apply custom button styling
        service_layout.addWidget(btn_file_converter)

        btn_digital_key = QPushButton('Digital Key Generator', self)
        btn_digital_key.clicked.connect(self.showDigitalKeyGenerator)  # Connect to digital key generator
        self.style_button(btn_digital_key)  # Apply custom button styling
        service_layout.addWidget(btn_digital_key)

        main_content_layout.addLayout(service_layout)

        self.layout.addLayout(main_content_layout)

        self.setLayout(self.layout)

        # Apply background color to the main page
        self.setStyleSheet('background-color: #f0f0f0;')

        # Initialize the stacked widget
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.addWidget(QWidget())  # Home placeholder
        self.stacked_widget.addWidget(QRCodeGenerator())
        self.stacked_widget.addWidget(ImageToTextConverter())
        self.stacked_widget.addWidget(FileConverter())
        self.stacked_widget.addWidget(DigitalKeyGenerator())

        main_content_layout.addWidget(self.stacked_widget)

    def style_navbar_button(self, button):
        button.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50; /* Green */
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
                background-color: #008CBA; /* Blue */
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainPage = MainPage()
    mainPage.show()
    sys.exit(app.exec_())
