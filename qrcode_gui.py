import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFileDialog, QApplication
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import qrcode
import os

class QRCodeGenerator(QWidget):
    def __init__(self, main_app=None, parent=None):
        super().__init__(parent)
        self.initUI()
        self.main_app = main_app

    def initUI(self):
        self.setWindowTitle('QR Code Generator')
        self.setMinimumSize(400, 400)  # Adjusted dimensions
        self.setStyleSheet("background-color: #f0f0f0; border: 2px solid #ccc; border-radius: 10px;")
        layout = QVBoxLayout()

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

        # Button to go back to home
        self.button_back = QPushButton('Back to Home', self)
        self.button_back.clicked.connect(self.goBackToHome)
        main_layout.addWidget(self.button_back, alignment=Qt.AlignCenter)

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
            border= 4,
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

        # Store the QR code in the database
        if self.main_app and self.main_app.user_id is not None:
            file_name = "qrcode.png"
            file_path = os.path.join(os.getcwd(), file_name)
            img.save(file_path)
            self.main_app.store_generated_file(self.main_app.user_id, file_name, file_path)

    def saveQRCode(self):
        if hasattr(self, 'qrcode_pixmap'):
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self, "Save QR Code", "", "PNG Files (*.png);;JPEG Files (*.jpg)", options=options)
            if fileName:
                self.qrcode_pixmap.save(fileName)
                QMessageBox.information(self, 'Success', f'QR Code saved as {fileName}')
        else:
            QMessageBox.warning(self, 'Error', 'Generate a QR code first.')

    def goBackToHome(self):
        if self.main_app:
            self.main_app.showMainPage()  # Call the method to show the main page
        else:
            QMessageBox.warning(self, 'Error', 'Main application reference not found.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    from main import MainApp
    main_app = MainApp()
    qr_generator = QRCodeGenerator(main_app=main_app)
    qr_generator.show()
    sys.exit(app.exec_())
