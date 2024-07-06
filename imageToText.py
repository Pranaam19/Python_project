import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
import pytesseract
from PIL import Image

class ImageToTextConverter(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image to Text Converter')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel('Upload an image to extract text:', self)
        layout.addWidget(self.label)

        self.button = QPushButton('Upload Image', self)
        self.button.clicked.connect(self.uploadImage)
        layout.addWidget(self.button)

        self.textbox = QTextEdit(self)
        self.textbox.setReadOnly(True)
        layout.addWidget(self.textbox)

        self.setLayout(layout)

    def uploadImage(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Images (*.png *.jpg *.jpeg)", options=options)
        if fileName:
            extracted_text = self.extractTextFromImage(fileName)
            self.textbox.setPlainText(extracted_text)

    def extractTextFromImage(self, image_path):
        text = pytesseract.image_to_string(Image.open(image_path))
        return text
