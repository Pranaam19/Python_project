import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFileDialog, QMessageBox, QApplication, QComboBox
from PyQt5.QtCore import Qt
from gtts import gTTS
import os

class TextToSpeechConverter(QWidget):
    def __init__(self, main_app=None, parent=None):
        super().__init__(parent)
        self.initUI()
        self.main_app = main_app

    def initUI(self):
        self.setWindowTitle('Text to Speech Converter')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Label for instructions
        self.label = QLabel('Enter text to convert to speech:', self)
        layout.addWidget(self.label)

        # Text box for input
        self.textbox = QLineEdit(self)
        layout.addWidget(self.textbox)

        # Dropdown for selecting voice
        self.voice_selector = QComboBox(self)
        self.voice_selector.addItem('English - US', 'en')
        self.voice_selector.addItem('English - UK', 'en-uk')
        self.voice_selector.addItem('French', 'fr')
        self.voice_selector.addItem('Spanish', 'es')
        layout.addWidget(self.voice_selector)

        # Button to convert text to speech
        self.button_convert = QPushButton('Convert to Speech', self)
        self.button_convert.clicked.connect(self.convertToSpeech)
        layout.addWidget(self.button_convert)

        # Button to go back to home
        self.button_back = QPushButton('Back to Home', self)
        self.button_back.clicked.connect(self.goBackToHome)
        layout.addWidget(self.button_back)

        self.setLayout(layout)

        # Apply styles
        self.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
                color: black;
            }
            QLineEdit {
                font-size: 14px;
                padding: 8px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: white;
            }
            QComboBox {
                font-size: 14px;
                padding: 8px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: white;
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

    def convertToSpeech(self):
        text = self.textbox.text()
        if not text.strip():
            QMessageBox.warning(self, 'Error', 'Please enter some text.')
            return

        selected_voice = self.voice_selector.currentData()
        tts = gTTS(text=text, lang=selected_voice)
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Audio File", "", "Audio Files (*.mp3)")
        if save_path:
            tts.save(save_path)
            QMessageBox.information(self, 'Success', f'Speech saved as {save_path}')

    def goBackToHome(self):
        if self.main_app:
            self.main_app.showMainPage()  # Call the method to show the main page
        else:
            QMessageBox.warning(self, 'Error', 'Main application reference not found.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    from main import MainApp
    main_app = MainApp()
    tts_converter = TextToSpeechConverter(main_app=main_app)
    tts_converter.show()
    sys.exit(app.exec_())
