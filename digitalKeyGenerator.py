import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
import hashlib

class DigitalKeyGenerator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Digital Key Generator')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel('Enter text to generate digital key:', self)
        layout.addWidget(self.label)

        self.textbox = QTextEdit(self)
        layout.addWidget(self.textbox)

        self.button = QPushButton('Generate Key', self)
        self.button.clicked.connect(self.generateKey)
        layout.addWidget(self.button)

        self.key_label = QLabel('Generated Key:', self)
        layout.addWidget(self.key_label)

        self.key_textbox = QTextEdit(self)
        self.key_textbox.setReadOnly(True)
        layout.addWidget(self.key_textbox)

        self.setLayout(layout)

    def generateKey(self):
        text = self.textbox.toPlainText()
        if not text.strip():
            QMessageBox.warning(self, 'Error', 'Please enter some text.')
            return

        key = hashlib.sha256(text.encode()).hexdigest()
        self.key_textbox.setPlainText(key)
