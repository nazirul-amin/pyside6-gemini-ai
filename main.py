import json
import sys
import time
import multiprocessing

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QTextEdit, QPushButton, QFileDialog, QGroupBox,
    QHBoxLayout, QMessageBox
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt
from io import BytesIO
from image_generator import generate_image_from_prompt
from recipe_generator import generate_recipe_from_prompt
from auto_translator import run_translation, stop_translation

class GeneratorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gen Ai App: Gemini")
        self.setGeometry(300, 300, 700, 700)

        # Create the layout and UI elements
        self.layout = QVBoxLayout()

        self.type_label = QLabel("Select Generation Type:")
        self.layout.addWidget(self.type_label)

        # Horizontal layout for the buttons
        button_layout = QHBoxLayout()

        # Button for Recipe Generation
        self.recipe_gen_button = QPushButton("Recipe Generation")
        self.recipe_gen_button.clicked.connect(lambda: self.set_generation_type("Recipe Generation"))
        button_layout.addWidget(self.recipe_gen_button)
        
        # Button for Text Translation
        self.translate_button = QPushButton("Text Translation")
        self.translate_button.clicked.connect(lambda: self.set_generation_type("Text Translation"))
        button_layout.addWidget(self.translate_button)
        
        # Button for Image Generation
        self.image_gen_button = QPushButton("Image Generation")
        self.image_gen_button.clicked.connect(lambda: self.set_generation_type("Image Generation"))
        button_layout.addWidget(self.image_gen_button)

        # Add the button layout to the main layout
        self.layout.addLayout(button_layout)

        self.group_box = QGroupBox()
        self.group_layout = QVBoxLayout()
        self.group_box.setLayout(self.group_layout)
        self.layout.addWidget(self.group_box)

        self.prompt_label = QLabel("Input:")
        self.group_layout.addWidget(self.prompt_label)

        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Type your prompt here...")
        self.group_layout.addWidget(self.prompt_input)

        # Add a button to upload an image for recipe generation
        self.upload_button = QPushButton("Upload Image")
        self.upload_button.setIcon(QIcon("icons/upload.png"))
        self.upload_button.clicked.connect(self.upload_image)
        self.group_layout.addWidget(self.upload_button)

        # Generate Button
        self.generate_button = QPushButton("Generate")
        self.generate_button.setIcon(QIcon("icons/magic-wand.png"))
        self.generate_button.clicked.connect(self.generate_content)
        self.group_layout.addWidget(self.generate_button)
        
        # Start Button (toggle button for start/stop)
        self.start_button = QPushButton("Start")
        self.start_button.setIcon(QIcon("icons/play.png"))
        self.start_button.clicked.connect(self.toggle_process)
        self.group_layout.addWidget(self.start_button)
        
        # Add a label to display the uploaded image
        self.image_display_label = QLabel("Uploaded Image:")
        self.group_layout.addWidget(self.image_display_label)

        # QLabel for showing the image
        self.uploaded_image_label = QLabel()
        self.uploaded_image_label.setAlignment(Qt.AlignCenter)
        self.group_layout.addWidget(self.uploaded_image_label)
        
        # Result display
        self.result_label = QLabel("Output:")
        self.result_label.setWordWrap(True)
        self.group_layout.addWidget(self.result_label)

        self.translator_output = QTextEdit()
        self.translator_output.setReadOnly(True)
        self.translator_output.setPlaceholderText("The results will be displayed here...")
        self.group_layout.addWidget(self.translator_output)
        
        # Result Output Box
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        self.result_output.setPlaceholderText("The results will be displayed here...")
        self.group_layout.addWidget(self.result_output)
        
        # Log Output Box
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setPlaceholderText("Log output will be displayed here...")
        self.layout.addWidget(self.log_output)

        self.setLayout(self.layout)

        # To store the uploaded image path
        self.image_path = None

        # Track whether the process is running
        self.autotranslator_process = None

        # Initialize the UI based on the default selection
        self.current_generation_type = "Recipe Generation"
        self.set_generation_type("Recipe Generation")
        self.log_output.hide()

    def set_generation_type(self, generation_type):
        """Update the UI based on the selected generation type."""
        self.log_message(f"Selected Generation Type: {generation_type}")
        
        self.current_generation_type = generation_type
        
        if generation_type == "Image Generation":
            self.prompt_label.show()
            self.prompt_input.show()
            self.generate_button.show()
            self.upload_button.hide()
            self.result_output.hide()
            self.image_display_label.hide()
            self.uploaded_image_label.hide()
            self.start_button.hide()
            self.translator_output.hide()
        elif generation_type == "Recipe Generation":
            self.prompt_label.hide()
            self.prompt_input.hide()
            self.generate_button.hide()
            self.start_button.hide()
            self.translator_output.hide()
            self.upload_button.show()
            self.result_output.show()
            self.image_display_label.show()
            self.uploaded_image_label.show()
        elif generation_type == "Text Translation":
            self.start_button.show()
            self.translator_output.show()
            self.generate_button.hide()
            self.upload_button.hide()
            self.result_output.hide()
            self.image_display_label.hide()
            self.uploaded_image_label.hide()
            self.prompt_label.hide()
            self.prompt_input.hide()

        # Update button styles based on the selected generation type
        self.update_button_styles()

    def update_button_styles(self):
        """Update button styles based on the selected generation type."""
        if self.current_generation_type == "Image Generation":
            self.image_gen_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #388E3C;
                }
                QPushButton:pressed {
                    background-color: #2E7D32;
                }
            """)
            self.recipe_gen_button.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #1565C0;
                }
            """)
            self.translate_button.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #1565C0;
                }
            """)
        elif self.current_generation_type == "Recipe Generation":
            self.recipe_gen_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #388E3C;
                }
                QPushButton:pressed {
                    background-color: #2E7D32;
                }
            """)
            self.image_gen_button.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #1565C0;
                }
            """)
            self.translate_button.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #1565C0;
                }
            """)
        else:
            self.translate_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #388E3C;
                }
                QPushButton:pressed {
                    background-color: #2E7D32;
                }
            """)
            self.image_gen_button.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #1565C0;
                }
            """)
            self.recipe_gen_button.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #1565C0;
                }
            """)

    def upload_image(self):
        """Open a file dialog to upload an image and store its path."""
        self.upload_button.setText("Uploading...")
        try:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)", options=options)
            if file_name:
                self.image_path = file_name
                self.log_message("Recipe generation started...")
                recipe_text = generate_recipe_from_prompt(self.image_path)
        finally:
            self.upload_button.setText("Upload Image")
            self.display_uploaded_image(file_name)
            self.log_message(recipe_text)
            self.log_message("Recipe generation completed successfully.")
            self.display_recipe(recipe_text)

    def display_uploaded_image(self, file_path):
        """Display the uploaded image in the QLabel."""
        try:
            pixmap = QPixmap(file_path)
            self.uploaded_image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
            self.uploaded_image_label.setScaledContents(False)
        except Exception as e:
            self.show_error_message(f"Failed to display uploaded image: {str(e)}")

    def generate_content(self):
        prompt = self.prompt_input.toPlainText()
        generation_type = self.current_generation_type

        # Disable the generate button and change its text
        self.generate_button.setEnabled(False)
        self.generate_button.setText("Generating...")
        
        self.log_message(f"Generating {generation_type} content...")

        QApplication.processEvents()

        try:
            if generation_type == "Image Generation":
                pil_image = generate_image_from_prompt(prompt)
                self.display_image(pil_image)

            elif generation_type == "Xunity Autotranslator":
                translated_text = self.translate_text(prompt)
                self.display_translation(prompt, translated_text)

        except Exception as e:
            self.show_error_message(f'Error: {str(e)}')
            self.log_message(f'<font color="red">Error occurred: {str(e)}</font>')

        finally:
            self.generate_button.setEnabled(True)
            self.generate_button.setText("Generate")

    def display_image(self, pil_image):
        """Display the generated image in the QLabel."""
        try:
            bytes_io = BytesIO()
            pil_image.save(bytes_io, format='PNG')
            bytes_io.seek(0)
            pixmap = QPixmap()
            pixmap.loadFromData(bytes_io.getvalue())
            self.uploaded_image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
            self.uploaded_image_label.setScaledContents(False)
        except Exception as e:
            self.show_error_message(f"Failed to display generated image: {str(e)}")
            
    def display_recipe(self, recipe_response):
        """Display the generated recipe text as a formatted recipe."""
        try:
            # Parse the JSON response directly
            recipe_data = json.loads(recipe_response)

            # Ensure we are handling the first item in the list
            if recipe_data:
                formatted_recipe = self.format_recipe(recipe_data[0])  # Access the first recipe item
                self.result_output.setPlainText(formatted_recipe)
                self.result_label.clear()
            else:
                self.show_error_message('No recipe data found.')
        except json.JSONDecodeError:
            self.show_error_message('Failed to parse JSON response.')
        except Exception as e:
            self.show_error_message(f'Failed to display recipe: {str(e)}')

    def format_recipe(self, recipe_data):
        """Format the recipe text from JSON into a readable format."""
        try:
            formatted_recipe = ""
            formatted_recipe += f"**Recipe Name:** {recipe_data['recipe_name']}\n\n"
            formatted_recipe += "### Ingredients:\n"
            
            for ingredient in recipe_data['ingredients']:
                formatted_recipe += f"- {ingredient}\n"

            formatted_recipe += "\n### Instructions:\n"
            for i, step in enumerate(recipe_data['instructions'], start=1):
                formatted_recipe += f"{i}. {step}\n"

            return formatted_recipe.strip()
        except Exception as e:
            raise Exception(f"Error formatting recipe: {str(e)}")
        
    def update_translator_output(self, output):
        self.translator_output.append(f"Output received: {output}")

    def toggle_process(self):
        """Start or stop the translator process using multiprocessing."""
        try:
            if self.start_button.text() == "Start":
                self.translator_output.append("Starting translation process...")
                self.autotranslator_process = multiprocessing.Process(target=run_translation)
                self.autotranslator_process.start()
                self.start_button.setText("Stop")
                self.start_button.setIcon(QIcon("icons/stop.png"))
                self.translator_output.append("Translation process started.")
            else:
                self.translator_output.append("Stopping translation process...")
                if self.autotranslator_process and self.autotranslator_process.is_alive():
                    stop_translation()
                    self.autotranslator_process.terminate()
                    self.autotranslator_process.join()
                self.start_button.setText("Start")
                self.start_button.setIcon(QIcon("icons/play.png"))
                self.translator_output.append("Translation process stopped.")
        except Exception as e:
            self.show_error_message(f'Failed to manage translation process: {str(e)}')
            self.translator_output.append(f'<font color="red">Failed to manage translation process: {str(e)}</font>')
        
    def show_error_message(self, message):
        """Show an error message dialog."""
        QMessageBox.critical(self, "Error", message)

    def log_message(self, message):
        """Log messages to the log output."""
        self.log_output.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GeneratorApp()
    window.show()
    sys.exit(app.exec())