#This is the file that the user ought to execute.

#Standard Libraries
import sys #Required for opening a window

#Third-Party Libraries
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QHBoxLayout, QVBoxLayout, QWidget #The library utilised for the GUI

#Local Libraries

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Havelock North Scout Hall — Inventory Management") #Sets the title of the window
        self.resize(800, 600)

        #QSS (Effectively CSS)
        basic_element: str = """background-color: #cccccc; 
                                color: black; 
                                padding: 10px; 
                                border: 2px solid black; 
                                border-radius: 16px;"""

        #Layouts
        main_columns = QHBoxLayout()
        left_side = QVBoxLayout()
        right_side = QVBoxLayout()

        #Set up title
        title_label = QLabel("<h1>Inventory Management</h1>") #Creates a heading for the output section
        title_label.setStyleSheet(basic_element)
        left_side.addWidget(title_label, alignment=Qt.AlignCenter)
        left_side.addStretch()

        #Adds both of the sides to the overall layout
        main_columns.addLayout(left_side)
        main_columns.addLayout(right_side)
        self.setLayout(main_columns) #Displays layout

app = QApplication(sys.argv)
print("running...")

widget = Widget()
widget.show()

app.exec()
