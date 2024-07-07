from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt

import qrcode

class QRCodeGenerator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QR Code Generator')
        self.setMinimumSize(400, 400)  # Adjusted dimensions
        self.setStyleSheet("background-color: #f0f0f0; border: 2px solid #ccc; border-radius: 10px;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title label
        title_label = QLabel('Generate QR Code', self)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        main_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Form layout for text input and buttons
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        self.label_text = QLabel('Enter text:', self)
        form_layout.addWidget(self.label_text, alignment=Qt.AlignLeft)

        self.textbox = QLineEdit(self)
        form_layout.addWidget(self.textbox)

        # Horizontal layout for buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.button_generate = QPushButton('Generate QR Code', self)
        self.button_generate.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; margin: 4px 2px; cursor: pointer; border-radius: 5px;")
        self.button_generate.clicked.connect(self.generateQRCode)
        button_layout.addWidget(self.button_generate)

        self.button_save = QPushButton('Save QR Code', self)
        self.button_save.setStyleSheet("background-color: #008CBA; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; margin: 4px 2px; cursor: pointer; border-radius: 5px;")
        self.button_save.clicked.connect(self.saveQRCode)
        button_layout.addWidget(self.button_save)

        form_layout.addLayout(button_layout)

        main_layout.addLayout(form_layout)

        # QR Code display area
        self.qr_label = QLabel(self)
        self.qr_label.setFixedSize(300, 300)
        self.qr_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.qr_label, alignment=Qt.AlignCenter)

        # Back to Home button
        self.button_back = QPushButton('Back to Home', self)
        self.button_back.setIcon(QIcon('back.png'))  # Assuming back.png is in the current directory
        self.button_back.clicked.connect(self.goToHomePage)
        main_layout.addWidget(self.button_back, alignment=Qt.AlignRight)

        self.setLayout(main_layout)

    def generateQRCode(self):
        text = self.textbox.text()
        if not text.strip():
            QMessageBox.warning(self, 'Error', 'Please enter some text.')
            return

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

        img = img.convert("RGB")  # Convert image to RGB
        data = img.tobytes("raw", "RGB")
        bytes_per_line = img.size[0] * 3  # 3 bytes per pixel for RGB
        qimage = QImage(data, img.size[0], img.size[1], bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)

        # Scale pixmap to fit QLabel, preserving aspect ratio
        scaledPixmap = pixmap.scaled(self.qr_label.width(), self.qr_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.qr_label.clear()
        self.qr_label.setPixmap(scaledPixmap)
        self.qr_label.adjustSize()

        self.qrcode_pixmap = pixmap  # Store the pixmap for saving

    def saveQRCode(self):
        if hasattr(self, 'qrcode_pixmap'):
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self, "Save QR Code", "", "PNG Files (*.png);;JPEG Files (*.jpg)", options=options)
            if fileName:
                self.qrcode_pixmap.save(fileName)
                QMessageBox.information(self, 'Success', f'QR Code saved as {fileName}')
        else:
            QMessageBox.warning(self, 'Error', 'Generate a QR code first.')

    def goToHomePage(self):
        if self.parent() and hasattr(self.parent(), 'showHomePage'):
            self.parent().showHomePage()
