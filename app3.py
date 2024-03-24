# Vertical box layout
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout


# Design window
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")
        
        #layout
        vbox = QVBoxLayout(self)
        self.setLayout(vbox)
        
        #button Widget
        btn1 = QPushButton("1")
        btn2 = QPushButton("2")
        btn3 = QPushButton("3")
        
        # format Widget in layout
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(btn3)
        
        
        
        
        
        
# run program
app = QCoreApplication.instance()

if app is None:
    app = QApplication([])
    
window = MainWindow()
window.show()
app.exec()

        
         