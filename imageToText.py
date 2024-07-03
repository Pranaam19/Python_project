import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QTextBrowser, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import pytesseract
from PIL import Image

class ImageToTextConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image to Text Converter')
        self.setGeometry(200, 200, 800, 600)

        self.layout = QVBoxLayout()

        # Upload button
        self.btn_upload = QPushButton('Upload Image', self)
        self.btn_upload.clicked.connect(self.uploadImage)
        self.layout.addWidget(self.btn_upload, alignment=Qt.AlignCenter)

        # Image display area
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        # Text display area
        self.text_browser = QTextBrowser(self)
        self.layout.addWidget(self.text_browser)

        self.setLayout(self.layout)

    def uploadImage(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Upload Image", "", "Image Files (*.png *.jpg *.jpeg *.gif)", options=options)
        if fileName:
            # Display selected image
            pixmap = QPixmap(fileName)
            self.image_label.setPixmap(pixmap.scaledToWidth(400))  # Adjust width as needed

            # Perform OCR using pytesseract
            extracted_text = self.extractTextFromImage(fileName)
            self.text_browser.setText(extracted_text)

    def extractTextFromImage(self, image_path):
        # Use pytesseract to perform OCR
        text = pytesseract.image_to_string(Image.open(image_path))
        return text

if __name__ == '__main__':
    app = QApplication(sys.argv)
    converter_page = ImageToTextConverter()
    converter_page.show()
    sys.exit(app.exec_())
