import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import sqlite3
import hashlib

class SignupPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Signup Page')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label_username = QLabel('Username:', self)
        self.textbox_username = QLineEdit(self)

        self.label_password = QLabel('Password:', self)
        self.textbox_password = QLineEdit(self)
        self.textbox_password.setEchoMode(QLineEdit.Password)

        self.button_signup = QPushButton('Sign Up', self)
        self.button_signup.clicked.connect(self.signup)

        layout.addWidget(self.label_username)
        layout.addWidget(self.textbox_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.textbox_password)
        layout.addWidget(self.button_signup)

        self.setLayout(layout)

    def signup(self):
        username = self.textbox_username.text()
        password = self.textbox_password.text()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)')
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        if c.fetchone():
            QMessageBox.warning(self, 'Error', 'Username already exists')
        else:
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            QMessageBox.information(self, 'Success', 'User registered successfully')
            self.parentWidget().showLoginPage()
        conn.close()
