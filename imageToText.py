import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit, QMessageBox, QApplication
from PyQt5.QtCore import Qt, QMimeData
import pytesseract
from PIL import Image

class ImageToTextConverter(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image to Text Converter')
        self.setMinimumSize(400, 300)  # Adjusted dimensions
        self.setStyleSheet("background-color: #f0f0f0; border: 2px solid #ccc; border-radius: 10px;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title label
        title_label = QLabel('Image to Text Converter', self)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        main_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Form layout for image upload and text display
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        self.label = QLabel('Upload an image:', self)
        form_layout.addWidget(self.label, alignment=Qt.AlignLeft)

        self.button = QPushButton('Upload Image', self)
        self.button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; margin: 4px 2px; cursor: pointer; border-radius: 5px;")
        self.button.clicked.connect(self.uploadImage)
        form_layout.addWidget(self.button)

        main_layout.addLayout(form_layout)

        # Text display area
        self.textbox = QTextEdit(self)
        self.textbox.setReadOnly(True)
        main_layout.addWidget(self.textbox)

        # Copy button
        self.button_copy = QPushButton('Copy Text', self)
        self.button_copy.setStyleSheet("background-color: #008CBA; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; margin: 4px 2px; cursor: pointer; border-radius: 5px;")
        self.button_copy.clicked.connect(self.copyText)
        main_layout.addWidget(self.button_copy)

        self.setLayout(main_layout)

    def uploadImage(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Images (*.png *.jpg *.jpeg)", options=options)
        if fileName:
            extracted_text = self.extractTextFromImage(fileName)
            self.textbox.setPlainText(extracted_text)

    def extractTextFromImage(self, image_path):
        text = pytesseract.image_to_string(Image.open(image_path))
        return text

    def copyText(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.textbox.toPlainText())
