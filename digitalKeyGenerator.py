import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QMessageBox, QApplication
from PyQt5.QtCore import Qt
import hashlib
from PyQt5.QtGui import QPalette, QBrush, QPixmap

class DigitalKeyGenerator(QWidget):
    def __init__(self,main_app=None, parent=None):
        super().__init__(parent)
        self.initUI()
        self.main_app = main_app

    def initUI(self):
        self.setWindowTitle('Digital Key Generator')
        self.setGeometry(100, 100, 400, 300)

        # Set background image
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("bg.jpg")))
        self.setPalette(palette)

        layout = QVBoxLayout()

        # Label for entering text
        self.label = QLabel('Enter text to generate digital key:', self)
        layout.addWidget(self.label)

        # Text box for input
        self.textbox = QTextEdit(self)
        layout.addWidget(self.textbox)

        # Button to generate key
        self.button_generate = QPushButton('Generate Key', self)
        self.button_generate.clicked.connect(self.generateKey)
        layout.addWidget(self.button_generate)

        # Label for generated key
        self.key_label = QLabel('Generated Key:', self)
        layout.addWidget(self.key_label)

        self.button_back = QPushButton('Back to Home', self)
        self.button_back.clicked.connect(self.goBackToHome)
        layout.addWidget(self.button_back)

        # Text box for displaying generated key (read-only)
        self.key_textbox = QTextEdit(self)
        self.key_textbox.setReadOnly(True)
        layout.addWidget(self.key_textbox)

        self.setLayout(layout)

        # Apply styles
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;  /* Make background transparent to show the image */
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
                color: white;  /* Adjust color for better visibility on the background */
            }
            QTextEdit {
                font-size: 14px;
                padding: 8px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: rgba(255, 255, 255, 0.8);  /* Semi-transparent background */
            }
            QPushButton {
                font-size: 14px;
                padding: 10px;
                margin-top: 10px;
                margin-bottom: 10px;
                background-color: #4CAF50;  /* Green */
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;  /* Darker green on hover */
            }
            QPushButton:pressed {
                background-color: #3e8e41;  /* Darker green when pressed */
            }
        """)

    def generateKey(self):
        text = self.textbox.toPlainText()
        if not text.strip():
            QMessageBox.warning(self, 'Error', 'Please enter some text.')
            return

        key = hashlib.sha256(text.encode()).hexdigest()
        self.key_textbox.setPlainText(key)

    def goBackToHome(self):
        if self.main_app:
            self.main_app.showMainPage()  # Call the method to show the main page
        else:
            QMessageBox.warning(self, 'Error', 'Main application reference not found.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    from main import MainApp
    main_app = MainApp()
    key_generator = DigitalKeyGenerator(main_app=main_app)
    key_generator.show()
    sys.exit(app.exec_())
