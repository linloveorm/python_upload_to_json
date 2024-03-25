from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QDialog, QScrollArea, QTextEdit
from ML_vision import main
import json
import os
import shutil

# Placeholder for database interaction
def store_data_in_database(json_data):
    try:
        # Simulate storing data in the database
        # Replace this with actual database interaction code
        print("Storing data in the database...")
        # Assume data is stored successfully in the database
        return True
    except Exception as e:
        print(f"Error storing data in the database: {e}")
        return False

class JsonDialog(QDialog):
    def __init__(self, json_data, file_path, database_connection):
        super().__init__()
        self.setWindowTitle("JSON Data")
        self.file_path = file_path  # Store the file path
        self.json_data = json_data  # Store the JSON data
        self.database_connection = database_connection

        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Allow resizing of the widget

        # Create a text edit widget to display JSON data
        self.json_text_edit = QTextEdit()
        self.json_text_edit.setReadOnly(True)  # Make the text edit widget read-only

        # Convert JSON data to a formatted string
        json_formatted = json.dumps(json_data, indent=4)
        self.json_text_edit.setPlainText(json_formatted)

        # Set the text edit widget as the scroll area's widget
        scroll_area.setWidget(self.json_text_edit)

        # Add the scroll area to the layout of the dialog
        layout = QVBoxLayout(self)
        layout.addWidget(scroll_area)

        # Create confirm and cancel buttons
        confirm_button = QPushButton("Correct")
        confirm_button.clicked.connect(self.save_file)  # Connect to save_file method
        layout.addWidget(confirm_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        layout.addWidget(cancel_button)

        # Create a label for displaying the status message
        self.status_label = QLabel()
        layout.addWidget(self.status_label)

    def save_file(self):
        # Copy the file to the "input" folder
        destination = os.path.join('input', os.path.basename(self.file_path))
        shutil.copyfile(self.file_path, destination)
        
        # Display "Storing data in the database..."
        self.status_label.setText("Storing data in the database...")

        # Simulate storing data in the database
        success = store_data_in_database(self.json_data)
        if success:
            # Display "Store data success" after a delay of 2 seconds
            QTimer.singleShot(2000, self.display_success_message)
        else:
            self.status_label.setText("Failed to store data in the database. Please check the database connection.")

    def display_success_message(self):
        # Display "Store data success"
        self.status_label.setText("Store data success")
        self.accept()  # Close the dialog after displaying the success message

class ErrorDialog(QDialog):
    def __init__(self, error_data):
        super().__init__()
        self.setWindowTitle("Error Data")
        layout = QVBoxLayout()
        self.error_label = QLabel()
        layout.addWidget(self.error_label)
        self.setLayout(layout)
        self.set_error_data(error_data)

    def set_error_data(self, error_data):
        if isinstance(error_data, list):
            error_data = str(error_data)
        self.error_label.setText(error_data)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python App")
        self.selected_file_path = None
        self.json_dialog = None

        vbox = QVBoxLayout(self)

        self.btn_browse = QPushButton("Browse")
        self.btn_browse.clicked.connect(self.browse_file)
        vbox.addWidget(self.btn_browse)

        self.lbl_selected_file = QLabel("Selected File: None")
        vbox.addWidget(self.lbl_selected_file)

        self.btn_run_ml = QPushButton("Run ML Vision")
        self.btn_run_ml.clicked.connect(self.run_ml_vision)
        self.btn_run_ml.setEnabled(False)
        vbox.addWidget(self.btn_run_ml)

        self.setLayout(vbox)

    def browse_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select a File")
        if file_path:
            self.selected_file_path = file_path
            self.lbl_selected_file.setText(f"Selected File: {file_path}")
            self.btn_run_ml.setEnabled(True)

    def run_ml_vision(self):
        if self.selected_file_path:
            json_data, error_data = main(self.selected_file_path)

            # Pass database connection to JsonDialog
            self.json_dialog = JsonDialog(json_data, self.selected_file_path, "database_connection")
            if self.json_dialog.exec() == QDialog.accepted:  # Check if the dialog was accepted
                print("File saved to input folder")
            
            # Display error dialog if error data is present
        if error_data:
            error_dialog = ErrorDialog(error_data)
            error_dialog.exec()

def create_output_folder():
    # Check if 'output' folder exists
    if not os.path.exists('output'):
        # Create 'output' folder if it doesn't exist
        os.makedirs('output')

def create_input_folder():
    # Check if 'output' folder exists
    if not os.path.exists('input'):
        # Create 'output' folder if it doesn't exist
        os.makedirs('input')

if __name__ == "__main__":
    # Create 'output' folder if it doesn't exist
    create_output_folder()
    create_input_folder()

    # Set up the connection to your non-SQL database
    # Example: database_connection = YourDatabaseClient(host='localhost', port=27017)

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()



















#_______________________________________ can use but need to receive json data from ML_vision.py________________________________________________________________________

# from PyQt6.QtCore import QCoreApplication, Qt
# from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog
# from ML_vision import main
# import os

# # Design window
# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Test")
        
#         # Layout
#         vbox = QVBoxLayout(self)
#         self.setLayout(vbox)
        
#         # Button Widgets
#         self.btn_browse = QPushButton("Browse")
#         self.btn_browse.clicked.connect(self.browse_file)
#         vbox.addWidget(self.btn_browse)
        
#         self.lbl_selected_file = QLabel("Selected File: None")
#         vbox.addWidget(self.lbl_selected_file)
        
#         self.btn_run_ml = QPushButton("Run ML Vision")
#         self.btn_run_ml.clicked.connect(self.run_ml_vision)
#         self.btn_run_ml.setEnabled(False)  # Initially disabled until file is selected
#         vbox.addWidget(self.btn_run_ml)
        
#         self.selected_file_path = None
        
#     def browse_file(self):
#         file_dialog = QFileDialog()
#         file_path, _ = file_dialog.getOpenFileName(self, "Select a File")
#         if file_path:
#             self.selected_file_path = file_path
#             self.lbl_selected_file.setText(f"Selected File: {file_path}")
#             self.btn_run_ml.setEnabled(True)  # Enable the "Run ML Vision" button after file is selected
        
#     def run_ml_vision(self):
#         if self.selected_file_path:
#             # Call the main function from ML_vision.py and pass the selected file path
#             main(self.selected_file_path)


# # Run program
# app = QCoreApplication.instance()

# if app is None:
#     app = QApplication([])
    
# window = MainWindow()
# window.show()
# app.exec()
