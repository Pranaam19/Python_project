import sys
import sqlite3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QApplication
from PyQt5.QtGui import QFont, QPalette, QBrush, QPixmap

class LoginPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_app = parent
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 400, 300)

        # Set background image
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("bg.jpg")))
        self.setPalette(palette)

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

        # Login button
        self.button_login = QPushButton('Login', self)
        self.button_login.setFont(QFont('Arial', 12))
        self.button_login.clicked.connect(self.login)
        layout.addWidget(self.button_login)

        # Signup button
        self.button_signup = QPushButton('Signup', self)
        self.button_signup.setFont(QFont('Arial', 12))
        self.button_signup.clicked.connect(self.showSignupPage)
        layout.addWidget(self.button_signup)

        self.setLayout(layout)

        # Apply styles
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;  /* Make background transparent to show the image */
            }
            QLabel, QLineEdit, QPushButton {
                background-color: rgba(255, 255, 255, 0.5);  /* Semi-transparent background for readability */
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
                border-radius: 5px;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
            }
            QPushButton {
                padding: 10px;
                margin-top: 10px;
                margin-bottom: 10px;
                background-color: #4CAF50;  /* Green */
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;  /* Darker green on hover */
            }
            QPushButton:pressed {
                background-color: #3e8e41;  /* Darker green when pressed */
            }
        """)

    def login(self):
        username = self.textbox_username.text()
        password = self.textbox_password.text()

        if self.authenticate(username, password):
            self.main_app.showMainPage()
        else:
            QMessageBox.warning(self, 'Error', 'Invalid username or password.')

    def authenticate(self, username, password):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        result = c.fetchone()
        conn.close()
        return result is not None

    def showSignupPage(self):
        self.main_app.showSignupPage()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec_())
