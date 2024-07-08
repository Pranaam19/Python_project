import sys
import sqlite3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QApplication
from PyQt5.QtGui import QFont

class SignupPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_app = parent
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Signup')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Username label and textbox
        self.label_username = QLabel('Username:', self)
        self.label_username.setFont(QFont('Arial', 12))
        layout.addWidget(self.label_username)

        self.textbox_username = QLineEdit(self)
        layout.addWidget(self.textbox_username)

        # Password label and textbox
        self.label_password = QLabel('Password:', self)
        self.label_password.setFont(QFont('Arial', 12))
        layout.addWidget(self.label_password)

        self.textbox_password = QLineEdit(self)
        self.textbox_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.textbox_password)

        # Signup button
        self.button_signup = QPushButton('Signup', self)
        self.button_signup.setFont(QFont('Arial', 12))
        self.button_signup.clicked.connect(self.signup)
        layout.addWidget(self.button_signup)

        self.setLayout(layout)

        # Apply styles
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;  /* Light gray background */
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            QLineEdit {
                font-size: 14px;
                padding: 8px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
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

    def signup(self):
        username = self.textbox_username.text()
        password = self.textbox_password.text()

        if self.create_user(username, password):
            QMessageBox.information(self, 'Success', 'Account created successfully.')
            self.main_app.showLoginPage()
        else:
            QMessageBox.warning(self, 'Error', 'Username already exists.')

    def create_user(self, username, password):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
        try:
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            success = True
        except sqlite3.IntegrityError:
            success = False
        conn.close()
        return success

if __name__ == '__main__':
    app = QApplication(sys.argv)
    signup_page = SignupPage()
    signup_page.show()
    sys.exit(app.exec_())
