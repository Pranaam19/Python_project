import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import sqlite3
import hashlib

class LoginPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login Page')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label_username = QLabel('Username:', self)
        self.textbox_username = QLineEdit(self)

        self.label_password = QLabel('Password:', self)
        self.textbox_password = QLineEdit(self)
        self.textbox_password.setEchoMode(QLineEdit.Password)

        self.button_login = QPushButton('Login', self)
        self.button_login.clicked.connect(self.login)

        self.button_signup = QPushButton('Sign Up', self)
        self.button_signup.clicked.connect(self.showSignupPage)

        layout.addWidget(self.label_username)
        layout.addWidget(self.textbox_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.textbox_password)
        layout.addWidget(self.button_login)
        layout.addWidget(self.button_signup)

        self.setLayout(layout)

    def login(self):
        username = self.textbox_username.text()
        password = self.textbox_password.text()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
        result = c.fetchone()
        conn.close()

        if result:
            self.parentWidget().showMainPage()
        else:
            QMessageBox.warning(self, 'Error', 'Invalid username or password')

    def showSignupPage(self):
        self.parentWidget().showSignupPage()
