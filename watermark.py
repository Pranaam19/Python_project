import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit, QTextEdit, QMessageBox, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image, ImageDraw, ImageFont

class WatermarkGenerator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Watermark Generator')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Label for instructions
        self.label = QLabel('Upload an image to add watermark:', self)
        layout.addWidget(self.label)

        # Button to upload image
        self.button_upload = QPushButton('Upload Image', self)
        self.button_upload.clicked.connect(self.uploadImage)
        layout.addWidget(self.button_upload)

        # Label for entering watermark text
        self.label_text = QLabel('Enter watermark text:', self)
        layout.addWidget(self.label_text)

        # Text box for watermark text
        self.textbox = QLineEdit(self)
        layout.addWidget(self.textbox)

        # Button to add watermark
        self.button_add = QPushButton('Add Watermark', self)
        self.button_add.clicked.connect(self.addWatermark)
        layout.addWidget(self.button_add)

        # Label to display image
        self.image_label = QLabel(self)
        layout.addWidget(self.image_label)

        self.setLayout(layout)

        # Apply styles
        self.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
                color: black;
            }
            QLineEdit {
                font-size: 14px;
                padding: 8px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: white;
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

    def uploadImage(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)
        if fileName:
            self.image_path = fileName
            pixmap = QPixmap(fileName)
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)
        else:
            self.image_path = None

    def addWatermark(self):
        if not hasattr(self, 'image_path') or not self.image_path:
            QMessageBox.warning(self, 'Error', 'Please upload an image first.')
            return

        text = self.textbox.text()
        if not text.strip():
            QMessageBox.warning(self, 'Error', 'Please enter watermark text.')
            return

        image = Image.open(self.image_path).convert("RGBA")
        txt = Image.new("RGBA", image.size, (255, 255, 255, 0))

        font = ImageFont.truetype("arial.ttf", 40)
        draw = ImageDraw.Draw(txt)

        # Use textbbox to get the bounding box of the text
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        width, height = image.size

        position = (width - text_width - 10, height - text_height - 10)
        draw.text(position, text, fill=(255, 255, 255, 128), font=font)

        watermarked = Image.alpha_composite(image, txt)
        watermarked = watermarked.convert("RGB")

        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Watermarked Image", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)
        if save_path:
            watermarked.save(save_path)
            QMessageBox.information(self, 'Success', f'Watermarked image saved as {save_path}')
            self.image_label.setPixmap(QPixmap(save_path))
            self.image_label.setScaledContents(True)