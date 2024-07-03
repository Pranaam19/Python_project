import sys
import qrcode
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtGui import QPixmap, QFont

class QRCodeGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QR Code Generator')
        self.setGeometry(100, 100, 600, 400)  # Larger size

        self.layout = QVBoxLayout()

        self.textbox = QLineEdit(self)
        self.textbox.setPlaceholderText('Enter text or URL')
        self.layout.addWidget(self.textbox)

        self.generate_button = QPushButton('Generate QR Code', self)
        self.generate_button.clicked.connect(self.generateQR)
        self.generate_button.setStyleSheet('''
            background-color: #4CAF50; /* Green */
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 5px;
        ''')
        self.layout.addWidget(self.generate_button)

        self.qr_label = QLabel(self)
        self.qr_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.qr_label)

        self.setLayout(self.layout)

        # Apply modern styling to the window
        self.setStyleSheet('''
            background-color: #f0f0f0;
            font-family: Arial, sans-serif;
            font-size: 14px;
            padding: 20px;
        ''')

    def generateQR(self):
        data = self.textbox.text()
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save('qrcode.png')  # Save QR code as an image (optional)
        pixmap = QPixmap('qrcode.png')
        self.qr_label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QRCodeGenerator()

    # Set a nicer font for the application
    font = QFont("Segoe UI", 14)
    app.setFont(font)

    window.show()
    sys.exit(app.exec_())
