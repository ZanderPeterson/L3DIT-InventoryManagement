#This is the file that the user ought to execute.

#Standard Libraries
import sys #Required for opening a window

#Third-Party Libraries
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QWidget #The library utilised for the GUI

#Local Libraries
import qss

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Havelock North Scout Hall — Inventory Management") #Sets the title of the window
        self.resize(800, 600)

        #Layouts
        main_columns = QHBoxLayout()
        left_side = QVBoxLayout()
        right_side = QVBoxLayout()

        #Set up title
        title_label = QLabel("<h1>Inventory Management</h1>") #Creates a heading for the output section
        title_label.setStyleSheet(qss.basic_element)
        left_side.addWidget(title_label, alignment=Qt.AlignCenter)
        left_side.addStretch()

        #Set up Search & Filtering
        search_and_filters_layout = QVBoxLayout()
        search_bar = QLabel("Search Bar [Placeholder]") #A placeholder for now
        search_bar.setStyleSheet(qss.basic_element)
        search_and_filters_layout.addWidget(search_bar, alignment=Qt.AlignCenter)
        right_side.addLayout(search_and_filters_layout)

        #Set up the inventory available/unavailable buttons
        available_inventory_filter_layout = QHBoxLayout()
        available_inventory_filter_label = QLabel("Sort By:")
        available_inventory_filter_label.setStyleSheet(qss.basic_element)
        available_inventory_filter_layout.addWidget(available_inventory_filter_label)
        self.show_available_inventory: bool = True #True = available inventory, False = unavailable inventory.

        self.available_inventory_button = QPushButton("Inventory Available")
        self.available_inventory_button.setStyleSheet(qss.inventory_available_button_style)
        self.available_inventory_button.clicked.connect(lambda: self.available_inventory_filter(True))
        self.available_inventory_button.setCheckable(True)
        available_inventory_filter_layout.addWidget(self.available_inventory_button)

        self.unavailable_inventory_button = QPushButton("Inventory Unavailable")
        self.unavailable_inventory_button.setStyleSheet(qss.inventory_unavailable_button_style)
        self.unavailable_inventory_button.clicked.connect(lambda: self.available_inventory_filter(False))
        self.unavailable_inventory_button.setCheckable(True)
        available_inventory_filter_layout.addWidget(self.unavailable_inventory_button)
        
        right_side.addLayout(available_inventory_filter_layout)
        right_side.addStretch()

        #Adds both of the sides to the overall layout
        main_columns.addLayout(left_side)
        main_columns.addLayout(right_side)
        self.setLayout(main_columns) #Displays layout

    def available_inventory_filter(self, available_inventory_button_pressed: bool):
        print(f"current={self.show_available_inventory}, pressed={available_inventory_button_pressed}")
        if (self.show_available_inventory and (not available_inventory_button_pressed)):
            print(f"switching from available —> not available")
            self.show_available_inventory = False
        elif ((not self.show_available_inventory) and available_inventory_button_pressed):
            print(f"switching from not available —> available")
            self.show_available_inventory = True
        self.available_inventory_button.setChecked(self.show_available_inventory)
        self.unavailable_inventory_button.setChecked(not self.show_available_inventory)

app = QApplication(sys.argv)
print("running...")

widget = Widget()
widget.show()

app.exec()
