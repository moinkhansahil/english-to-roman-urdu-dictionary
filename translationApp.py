import sys
import csv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout, QFileDialog, QMessageBox, QDialog, QFormLayout
)
import pygame
import pyperclip

class AddTranslationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add New Translation')
        
        self.layout = QVBoxLayout()
        
        self.form_layout = QFormLayout()
        self.english_word_input = QLineEdit()
        self.urdu_translation_input = QLineEdit()
        
        self.form_layout.addRow('English Word:', self.english_word_input)
        self.form_layout.addRow('Urdu Translation:', self.urdu_translation_input)
        
        self.layout.addLayout(self.form_layout)
        
        self.add_button = QPushButton('Add')
        self.add_button.clicked.connect(self.accept)
        self.layout.addWidget(self.add_button)
        
        self.setLayout(self.layout)
        
    def get_translation(self):
        return self.english_word_input.text(), self.urdu_translation_input.text()

class TranslationApp(QWidget):
    def __init__(self, translation_file_path):
        super().__init__()
        self.setWindowTitle('English to Urdu Dictionary')
        self.setGeometry(100, 100, 800, 600)  # Setting window position and size

        # Load dictionary from the specified CSV file path
        self.translation_file_path = translation_file_path
        self.english_to_urdu = self.load_dictionary_from_csv(translation_file_path)

        # Initialize pygame for sound
        pygame.init()

        # Load sound effects
        self.sound_translate = pygame.mixer.Sound('sound_translate.wav')
        self.sound_add = pygame.mixer.Sound('sound_add.wav')
        self.sound_multiple = pygame.mixer.Sound('sound_multiple.wav')
        self.sound_process = pygame.mixer.Sound('sound_process.wav')
        self.sound_welcome = pygame.mixer.Sound('welcome.wav')

        # Play welcome sound
        self.sound_welcome.play()

        # Widgets
        self.input_word = QLineEdit()
        self.input_word.setPlaceholderText("Type an English word")

        self.translation_label = QLabel("Translation:")
        self.translation_result_label = QLineEdit()
        self.translation_result_label.setReadOnly(True)
        self.translation_result_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        translate_button = QPushButton('Translate')
        translate_button.clicked.connect(self.translate_word)

        copy_button = QPushButton('Copy')
        copy_button.clicked.connect(self.copy_translation)

        add_translation_button = QPushButton('Add New Translation')
        add_translation_button.clicked.connect(self.add_new_translation)

        multiple_words_button = QPushButton('Multiple Words Translation')
        multiple_words_button.clicked.connect(self.show_multiple_translation_fields)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Loaded translation file: {translation_file_path}"))
        layout.addWidget(QLabel("Enter an English word to translate:"))
        layout.addWidget(self.input_word)
        layout.addWidget(translate_button)
        layout.addWidget(copy_button)
        layout.addWidget(self.translation_label)
        layout.addWidget(self.translation_result_label)

        # Adding buttons to a horizontal layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_translation_button)
        button_layout.addWidget(multiple_words_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Apply styles
        self.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
            }
            QLineEdit {
                font-size: 16px;
            }
            QPushButton {
                font-size: 16px;
                padding: 8px;
            }
        """)

    def load_dictionary_from_csv(self, file_path):
        english_to_urdu = {}
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    english_word, urdu_translation = row
                    english_to_urdu[english_word.strip().lower()] = urdu_translation.strip()
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except IOError as e:
            print(f"Error: Unable to read file '{file_path}': {e}")
        except Exception as e:
            print(f"Error: An error occurred while loading the dictionary: {e}")
        return english_to_urdu

    def translate_word(self):
        word = self.input_word.text().strip().lower()
        translation = self.english_to_urdu.get(word, "empty")

        # Play sound effect
        self.sound_translate.play()

        # Format the output as "hello translation is 'salam'"
        output_message = f'{word} translation is "{translation}"'

        self.translation_result_label.setText(output_message)

    def copy_translation(self):
        translation = self.translation_result_label.text()
        pyperclip.copy(translation)
        QMessageBox.information(self, "Copied", "Translation copied to clipboard!")

    def add_new_translation(self):
        # Play sound effect
        self.sound_add.play()

        dialog = AddTranslationDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            english_word, urdu_translation = dialog.get_translation()
            if english_word and urdu_translation:
                self.english_to_urdu[english_word.lower()] = urdu_translation
                self.save_new_translation_to_csv(english_word, urdu_translation)
            else:
                QMessageBox.warning(self, "Invalid Input", "Both English and Urdu translations are required.")

    def save_new_translation_to_csv(self, english_word, urdu_translation):
        try:
            with open(self.translation_file_path, mode='a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([english_word, urdu_translation])
                QMessageBox.information(self, "Success", "New translation added successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save new translation: {e}")

    def show_multiple_translation_fields(self):
        # Play sound effect
        self.sound_multiple.play()

        self.multiple_words_dialog = QDialog(self)
        self.multiple_words_dialog.setWindowTitle('Multiple Words Translation')

        self.multiple_words_layout = QVBoxLayout()
        self.multiple_words_inputs = []

        for i in range(5):
            input_field = QLineEdit()
            input_field.setPlaceholderText(f"Type word {i+1}")
            self.multiple_words_layout.addWidget(input_field)
            self.multiple_words_inputs.append(input_field)

        process_button = QPushButton('Process')
        process_button.clicked.connect(self.process_multiple_words)
        self.multiple_words_layout.addWidget(process_button)

        self.multiple_words_dialog.setLayout(self.multiple_words_layout)
        self.multiple_words_dialog.exec_()

    def process_multiple_words(self):
        # Play sound effect
        self.sound_process.play()

        results = []
        for input_field in self.multiple_words_inputs:
            word = input_field.text().strip().lower()
            translation = self.english_to_urdu.get(word, "empty")
            
            output_message = f'{word} translation is "{translation}"'
            results.append(output_message)

        result_message = "\n".join(results)
        QMessageBox.information(self, "Translations", result_message)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Specify the file path where your translation file (CSV) is located
    translation_file_path = r'c:\users\dc\vv\english_to_roman_urdu.csv'

    window = TranslationApp(translation_file_path)
    window.show()
    sys.exit(app.exec_())
