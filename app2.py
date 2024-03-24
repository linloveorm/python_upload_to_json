# windows in class format
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton


# Design window
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")
        lb = QLabel("Hello Python", self)
        lb.move(150, 150) #move (x, y)
        btn = QPushButton("Click", self)
        btn.move(150, 200) #move (x, y)
        
        
        
        
# run program
app = QCoreApplication.instance()

if app is None:
    app = QApplication([])
    
window = MainWindow()
window.show()
app.exec()

        
         