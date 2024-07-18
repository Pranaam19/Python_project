import sqlite3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QListWidget, QHBoxLayout

class AdminPage(QWidget):
    def __init__(self, main_app=None, parent=None):
        super().__init__(parent)
        self.main_app = main_app
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Admin Page')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.user_list = QListWidget(self)
        self.load_users()
        layout.addWidget(self.user_list)

        form_layout = QFormLayout()
        self.new_username_input = QLineEdit()
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow('New Username:', self.new_username_input)
        form_layout.addRow('New Password:', self.new_password_input)

        add_user_button = QPushButton('Add User')
        add_user_button.clicked.connect(self.add_user)
        form_layout.addWidget(add_user_button)

        delete_user_button = QPushButton('Delete Selected User')
        delete_user_button.clicked.connect(self.delete_user)
        form_layout.addWidget(delete_user_button)

        layout.addLayout(form_layout)

        self.setLayout(layout)

    def load_users(self):
        self.user_list.clear()
        cursor = self.main_app.conn.cursor()
        cursor.execute('SELECT id, username FROM users')
        users = cursor.fetchall()
        for user in users:
            self.user_list.addItem(f"{user[0]}: {user[1]}")

    def add_user(self):
        username = self.new_username_input.text()
        password = self.new_password_input.text()

        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please fill in all fields')
            return

        cursor = self.main_app.conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            self.main_app.conn.commit()
            QMessageBox.information(self, 'Success', 'User added successfully')
            self.load_users()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, 'Error', 'Username already exists')

    def delete_user(self):
        selected_user = self.user_list.currentItem()
        if selected_user:
            user_id = int(selected_user.text().split(':')[0])
            cursor = self.main_app.conn.cursor()
            cursor.execute('DELETE FROM users WHERE id=?', (user_id,))
            self.main_app.conn.commit()
            QMessageBox.information(self, 'Success', 'User deleted successfully')
            self.load_users()
        else:
            QMessageBox.warning(self, 'Error', 'No user selected')
