import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
import pytesseract
from PIL import Image
import os

class ImageToTextConverter(QWidget):
    def __init__(self, main_app=None, parent=None):
        super().__init__(parent)
        self.initUI()
        self.main_app = main_app

    def initUI(self):
        self.setWindowTitle('Image to Text Converter')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.label = QLabel('Image to Text Converter', self)
        layout.addWidget(self.label)

        self.select_button = QPushButton('Select Image', self)
        self.select_button.clicked.connect(self.selectImage)
        layout.addWidget(self.select_button)

        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)

        # Button to go back to home
        self.button_back = QPushButton('Back to Home', self)
        self.button_back.clicked.connect(self.goBackToHome)
        layout.addWidget(self.button_back)

        self.setLayout(layout)
        self.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
                color: black;
            }
            QPushButton {
                font-size: 16px;
                padding: 10px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTextEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        """)

    def selectImage(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp);;All Files (*)", options=options)
        if fileName:
            self.processImage(fileName)

    def processImage(self, file_path):
        try:
            text = pytesseract.image_to_string(Image.open(file_path))
            self.text_edit.setPlainText(text)

            # Store the file in the database
            if self.main_app and self.main_app.user_id is not None:
                user_id = self.main_app.user_id
                file_name = os.path.basename(file_path)
                self.main_app.store_generated_file(user_id, file_name, file_path)
            else:
                QMessageBox.warning(self, 'Error', 'Main application reference or user ID not found.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"An error occurred while processing the image: {str(e)}")

    def goBackToHome(self):
        if self.main_app:
            self.main_app.showMainPage()  # Call the method to show the main page
        else:
            QMessageBox.warning(self, 'Error', 'Main application reference not found.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    from main import MainApp
    main_app = MainApp()
    converter = ImageToTextConverter(main_app=main_app)
    converter.show()
    sys.exit(app.exec_())
