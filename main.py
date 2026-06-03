#This is the file that the user ought to execute.

#Standard Libraries
import sys #Required for opening a window

#Third-Party Libraries
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QWidget #The library utilised for the GUI

#Local Libraries

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Havelock North Scout Hall — Inventory Management") #Sets the title of the window
        self.resize(800, 600)

        #QSS (Effectively CSS)
        #Due to the use of f-strings, double curly brackets must be used where normally only one would be required.
        basic_element: str = f"""
            background-color: #cccccc; 
            color: black; 
            padding: 10px; 
            border: 2px solid black; 
            border-radius: 16px;
        """
        basic_button_hover: str = f"""
            border-color: #5555cc;
        """
        basic_button_pressed: str = f"""
            border-color: #5555cc;
        """
        inventory_available_button_style: str = f"""
            QPushButton {{
                {basic_element}
                background-color: #aaffaa;
            }}
            QPushButton:hover {{
                {basic_button_hover}
                
            }}
            QPushButton:pressed {{
                {basic_button_pressed}
                background-color: #55ff55;
            }}
        """
        inventory_unavailable_button_style: str = f"""
            QPushButton {{
                {basic_element}
                background-color: #ffaaaa;
            }}
            QPushButton:hover {{
                {basic_button_hover}

            }}
            QPushButton:pressed {{
                {basic_button_pressed}
                background-color: #ff5555;
            }}
        """

        #Layouts
        main_columns = QHBoxLayout()
        left_side = QVBoxLayout()
        right_side = QVBoxLayout()

        #Set up title
        title_label = QLabel("<h1>Inventory Management</h1>") #Creates a heading for the output section
        title_label.setStyleSheet(basic_element)
        left_side.addWidget(title_label, alignment=Qt.AlignCenter)
        left_side.addStretch()

        #Set up Search & Filtering
        search_and_filters_layout = QVBoxLayout()
        search_bar = QLabel("Search Bar [Placeholder]")
        search_bar.setStyleSheet(basic_element + "min-height: 30px;")
        search_and_filters_layout.addWidget(search_bar, alignment=Qt.AlignCenter)
        right_side.addLayout(search_and_filters_layout)

        available_inventory_filter_layout = QHBoxLayout()
        available_inventory_filter_label = QLabel("Sort By:")
        available_inventory_filter_label.setStyleSheet(basic_element)
        available_inventory_filter_layout.addWidget(available_inventory_filter_label)
        available_inventory_button = QPushButton("Inventory Available")
        available_inventory_button.setStyleSheet(inventory_available_button_style)
        available_inventory_filter_layout.addWidget(available_inventory_button)
        unavailable_inventory_button = QPushButton("Inventory Unavailable")
        unavailable_inventory_button.setStyleSheet(inventory_unavailable_button_style)
        available_inventory_filter_layout.addWidget(unavailable_inventory_button)
        right_side.addLayout(available_inventory_filter_layout)
        right_side.addStretch()

        #Adds both of the sides to the overall layout
        main_columns.addLayout(left_side)
        main_columns.addLayout(right_side)
        self.setLayout(main_columns) #Displays layout

app = QApplication(sys.argv)
print("running...")

widget = Widget()
widget.show()

app.exec()
