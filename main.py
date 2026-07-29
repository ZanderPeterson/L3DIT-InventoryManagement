#This is the file that the user ought to execute.

#Standard Libraries
import sys #Required for opening a window

#Third-Party Libraries
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
                               QHBoxLayout, QVBoxLayout, QWidget, QSizePolicy) #The library utilised for the GUI

#Local Libraries
import qss

class MainWidget(QWidget):
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
        search_bar = QLineEdit()
        search_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        search_bar.setStyleSheet(qss.basic_element)
        right_side.addWidget(search_bar)

        #Set up the inventory available/unavailable buttons
        available_inventory_filter_layout = QHBoxLayout()
        available_inventory_filter_label = QLabel("Sort By:")
        available_inventory_filter_label.setStyleSheet(qss.basic_element)
        available_inventory_filter_layout.addWidget(available_inventory_filter_label, stretch=2)
        self.show_available_inventory: bool = True #True = available inventory, False = unavailable inventory.

        self.available_inventory_button = QPushButton("Inventory Available")
        self.available_inventory_button.setStyleSheet(qss.inventory_available_button_style)
        self.available_inventory_button.clicked.connect(lambda: self.available_inventory_filter(True))
        self.available_inventory_button.setCheckable(True)
        available_inventory_filter_layout.addWidget(self.available_inventory_button, stretch=3)

        self.unavailable_inventory_button = QPushButton("Inventory Unavailable")
        self.unavailable_inventory_button.setStyleSheet(qss.inventory_unavailable_button_style)
        self.unavailable_inventory_button.clicked.connect(lambda: self.available_inventory_filter(False))
        self.unavailable_inventory_button.setCheckable(True)
        available_inventory_filter_layout.addWidget(self.unavailable_inventory_button, stretch=3)

        right_side.addLayout(available_inventory_filter_layout)

        #Set up the issue filter buttons
        issue_filter_layout = QHBoxLayout()
        issue_filter_label = QLabel("Sort By:")
        issue_filter_label.setStyleSheet(qss.basic_element)
        issue_filter_layout.addWidget(issue_filter_label, stretch=1)
        self.show_issues: int = 0 #noissues = 0, issues = 1, all = 2

        self.noissues_filter_button = QPushButton("No Issues")
        self.noissues_filter_button.setStyleSheet(qss.noissues_button_style)
        self.noissues_filter_button.setCheckable(True)
        self.noissues_filter_button.clicked.connect(lambda: self.issues_filter(0))
        issue_filter_layout.addWidget(self.noissues_filter_button, stretch=1)

        self.issues_filter_button = QPushButton("Issues")
        self.issues_filter_button.setStyleSheet(qss.issues_button_style)
        self.issues_filter_button.setCheckable(True)
        self.issues_filter_button.clicked.connect(lambda: self.issues_filter(1))
        issue_filter_layout.addWidget(self.issues_filter_button, stretch=1)

        self.all_filter_button = QPushButton("All")
        self.all_filter_button.setStyleSheet(qss.all_button_style)
        self.all_filter_button.setCheckable(True)
        self.all_filter_button.clicked.connect(lambda: self.issues_filter(2))
        issue_filter_layout.addWidget(self.all_filter_button, stretch=1)

        right_side.addLayout(issue_filter_layout)

        #Display List o' Items
        self.itemlistwidget = QWidget()
        self.itemlistwidget.setStyleSheet(qss.item_list_available)
        self.itemlistlayout = QVBoxLayout()
        self.itemlistwidget.setLayout(self.itemlistlayout)

        self.testlabel = QLabel("Test")
        self.testlabel.setStyleSheet(qss.basic_element)
        self.itemlistlayout.addWidget(self.testlabel)
        self.itemlistlayout.addStretch()

        right_side.addWidget(self.itemlistwidget)

        #Adds both of the sides to the overall layout
        main_columns.addLayout(left_side, stretch=1)
        main_columns.addLayout(right_side, stretch=1)

        #Sets the default states of buttons
        self.available_inventory_filter(self.show_available_inventory)
        self.issues_filter(self.show_issues)  # Ensures one option is selected initially

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

        if self.show_available_inventory:
            self.itemlistwidget.setStyleSheet(qss.item_list_available)
            self.testlabel.show()
        else:
            self.itemlistwidget.setStyleSheet(qss.item_list_unavailable)
            self.testlabel.hide()

    def issues_filter(self, issues_filter_pressed: int):
        print("test")
        self.show_issues = issues_filter_pressed
        self.noissues_filter_button.setChecked(self.show_issues == 0)
        self.issues_filter_button.setChecked(self.show_issues == 1)
        self.all_filter_button.setChecked(self.show_issues == 2)

app = QApplication(sys.argv)
print("running...")

widget = MainWidget()
widget.show()

app.exec()
