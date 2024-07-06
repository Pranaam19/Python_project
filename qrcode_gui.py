from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
import qrcode
from PIL import Image

class QRCodeGenerator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QR Code Generator')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel('Enter text to generate QR Code:', self)
        layout.addWidget(self.label)

        self.textbox = QLineEdit(self)
        layout.addWidget(self.textbox)

        self.button = QPushButton('Generate QR Code', self)
        self.button.clicked.connect(self.generateQRCode)
        layout.addWidget(self.button)

        self.qr_label = QLabel(self)
        layout.addWidget(self.qr_label)

        self.setLayout(layout)

    def generateQRCode(self):
        text = self.textbox.text()
        if not text.strip():
            QMessageBox.warning(self, 'Error', 'Please enter some text.')
            return

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

        img = img.convert("RGB")  # Convert image to RGB
        data = img.tobytes("raw", "RGB")
        qimage = QImage(data, img.size[0], img.size[1], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)

        self.qr_label.setPixmap(pixmap)
