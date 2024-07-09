import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image
import cv2
import numpy as np

class WatermarkRemoval(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Watermark Removal')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.upload_button = QPushButton('Upload Image', self)
        self.upload_button.clicked.connect(self.uploadImage)
        layout.addWidget(self.upload_button)

        self.remove_button = QPushButton('Remove Watermark', self)
        self.remove_button.clicked.connect(self.removeWatermark)
        layout.addWidget(self.remove_button)

        self.save_button = QPushButton('Save Image', self)
        self.save_button.clicked.connect(self.saveImage)
        layout.addWidget(self.save_button)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        self.setLayout(layout)

        self.image_path = None
        self.processed_image = None

    def uploadImage(self):
        self.image_path, _ = QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Images (*.png *.jpg *.jpeg *.bmp)')
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            self.image_label.setPixmap(pixmap)

    def removeWatermark(self):
        if not self.image_path:
            QMessageBox.warning(self, 'Input Error', 'Please upload an image first.')
            return

        image = cv2.imread(self.image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        mask = cv2.inpaint(image, binary, 3, cv2.INPAINT_TELEA)

        self.processed_image = mask
        processed_image_path = 'processed_image.png'
        cv2.imwrite(processed_image_path, mask)

        pixmap = QPixmap(processed_image_path)
        self.image_label.setPixmap(pixmap)

        self.saveImage(processed_image_path)

    def saveImage(self, processed_image_path):
        user_id = self.parent().parent().user_id
        if user_id and processed_image_path:
            file_name = os.path.basename(processed_image_path)
            file_path = os.path.abspath(processed_image_path)
            self.parent().parent().store_generated_file(user_id, file_name, file_path)
            QMessageBox.information(self, 'Success', 'Image saved successfully.')
        else:
            QMessageBox.warning(self, 'Error', 'Unable to save image.')
