#This is the file that the user ought to execute.

#Standard Libraries
import sys #Required for opening a window

#Third-Party Libraries
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
                               QHBoxLayout, QVBoxLayout, QWidget, QSizePolicy) #The library utilised for the GUI

#Local Libraries
import qss
from local_data import data_utils

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Havelock North Scout Hall — Inventory Management") #Sets the title of the window
        self.resize(800, 600)
        data_utils.add_uuids_to_items() #If any new items are added, adds UUIDs to them

        #Layouts
        main_columns = QHBoxLayout()
        left_side = QVBoxLayout()
        right_side = QVBoxLayout()

        #Set up title
        title_label = QLabel("<h1>Inventory Management</h1>") #Creates a heading for the output section
        title_label.setStyleSheet(qss.basic_element)
        left_side.addWidget(title_label, alignment=Qt.AlignCenter)

        #Set up Search & Filtering
        self.search_bar = QLineEdit()
        self.search_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.search_bar.setStyleSheet(qss.basic_element)
        self.search_bar.textChanged.connect(lambda _: self.render_item_list())
        right_side.addWidget(self.search_bar)

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
        self.rendered_items: dict[str, dict[QWidget]] = {}
        self.no_items_popup = QLabel("No items matched your search")
        self.no_items_popup.setStyleSheet(qss.basic_element)
        self.no_items_popup.setVisible(False)
        self.itemlistlayout.addWidget(self.no_items_popup)
        self.itemlistlayout.addStretch()
        right_side.addWidget(self.itemlistwidget)

        #Display the Info Panel
        self.infopanelwidget = QWidget()
        self.infopanelwidget.setStyleSheet(qss.basic_element)
        self.infopanelwidget.setContentsMargins(12, 12, 12, 12)
        self.infopanellayout = QVBoxLayout()
        self.infopanelwidget.setLayout(self.infopanellayout)
        self.info_panel_info: dict[str, dict[QWidget]] = {}
        self.infopanellayout.addStretch()
        left_side.addWidget(self.infopanelwidget)

        #Adds both of the sides to the overall layout
        main_columns.addLayout(left_side, stretch=1)
        main_columns.addLayout(right_side, stretch=1)

        #Sets the default states of buttons
        self.available_inventory_filter(self.show_available_inventory)
        self.issues_filter(self.show_issues)  # Ensures one option is selected initially

        self.setLayout(main_columns) #Displays layout

    def render_item_list(self):
        """
        Renders all items in item screen.
        """
        for item in self.rendered_items.values():
            item["QWidget"].deleteLater()
        self.rendered_items = {}

        items: List[str] = data_utils.get_items(self.show_available_inventory, self.search_bar.text())
        self.no_items_popup.setVisible(len(items) == 0) #Shows the "no items" popup if no items are found
        for item_uuid in items:
            self.rendered_items[item_uuid] = {}
            self.rendered_items[item_uuid]["QWidget"] = QWidget()
            self.rendered_items[item_uuid]["QWidget"].setStyleSheet(qss.item_in_list)
            self.rendered_items[item_uuid]["Layout"] = QHBoxLayout()
            self.rendered_items[item_uuid]["Layout"].setContentsMargins(10, 0, 0, 0)

            self.rendered_items[item_uuid]["ButtonLabel"] = QPushButton(data_utils.get_item_information(item_uuid)["name"])
            self.rendered_items[item_uuid]["ButtonLabel"].setStyleSheet(qss.item_label)
            self.rendered_items[item_uuid]["ButtonLabel"].clicked.connect(lambda _, uuid=item_uuid: self.display_info(uuid))
            self.rendered_items[item_uuid]["Layout"].addWidget(self.rendered_items[item_uuid]["ButtonLabel"], stretch=2)
            self.rendered_items[item_uuid]["CheckWidget"] = QWidget()

            if self.show_available_inventory:
                self.rendered_items[item_uuid]["CheckWidgetButton"] = QPushButton("Check Out")
                self.rendered_items[item_uuid]["CheckWidgetButton"].setStyleSheet(qss.item_checkout_button)
                self.rendered_items[item_uuid]["CheckWidgetButton"].clicked.connect(lambda _, uuid=item_uuid: self.check_out(uuid))
            else:
                self.rendered_items[item_uuid]["CheckWidgetButton"] = QPushButton("Check In")
                self.rendered_items[item_uuid]["CheckWidgetButton"].setStyleSheet(qss.item_checkin_button)
                self.rendered_items[item_uuid]["CheckWidgetButton"].clicked.connect(lambda _, uuid=item_uuid: self.check_in(uuid))
            self.rendered_items[item_uuid]["CheckWidgetLayout"] = QHBoxLayout()
            self.rendered_items[item_uuid]["CheckWidgetLayout"].setContentsMargins(0, 0, 0, 0)
            self.rendered_items[item_uuid]["CheckWidgetLayout"].addWidget(self.rendered_items[item_uuid]["CheckWidgetButton"])
            self.rendered_items[item_uuid]["CheckWidget"].setLayout(self.rendered_items[item_uuid]["CheckWidgetLayout"])

            self.rendered_items[item_uuid]["Layout"].addWidget(self.rendered_items[item_uuid]["CheckWidget"], stretch=1)
            self.rendered_items[item_uuid]["QWidget"].setLayout(self.rendered_items[item_uuid]["Layout"])
            insert_widget_location = max(0, self.itemlistlayout.count()-1) #Ensures widget is before stretch
            self.itemlistlayout.insertWidget(insert_widget_location, self.rendered_items[item_uuid]["QWidget"])

    def available_inventory_filter(self, available_inventory_button_pressed: bool):
        if (self.show_available_inventory and (not available_inventory_button_pressed)):
            self.show_available_inventory = False
        elif ((not self.show_available_inventory) and available_inventory_button_pressed):
            self.show_available_inventory = True
        self.available_inventory_button.setChecked(self.show_available_inventory)
        self.unavailable_inventory_button.setChecked(not self.show_available_inventory)

        if self.show_available_inventory:
            self.itemlistwidget.setStyleSheet(qss.item_list_available)
        else:
            self.itemlistwidget.setStyleSheet(qss.item_list_unavailable)
        self.render_item_list()

    def issues_filter(self, issues_filter_pressed: int):
        self.show_issues = issues_filter_pressed
        self.noissues_filter_button.setChecked(self.show_issues == 0)
        self.issues_filter_button.setChecked(self.show_issues == 1)
        self.all_filter_button.setChecked(self.show_issues == 2)

    def check_in(self, uuid:str):
        data_utils.modify_item_information(uuid, {"availability": "Available"})
        self.render_item_list()
        self.display_info(uuid)

    def check_out(self, uuid:str):
        #Replaces Check Out Button on Item with Text Field (for name entry)
        self.rendered_items[uuid]["CheckWidgetButton"].deleteLater() #Removes the button
        self.rendered_items[uuid]["CheckWidgetNameField"] = QLineEdit()
        self.rendered_items[uuid]["CheckWidgetNameField"].setStyleSheet(qss.item_checkout_field)
        self.rendered_items[uuid]["CheckWidgetNameField"].setPlaceholderText("Enter Name...")
        self.rendered_items[uuid]["CheckWidgetNameField"].textChanged.connect(lambda: self.on_check_out_field_change(uuid, "Item"))
        self.rendered_items[uuid]["CheckWidgetNameField"].returnPressed.connect(lambda: self.complete_check_out(uuid))
        self.rendered_items[uuid]["CheckWidgetLayout"].addWidget(self.rendered_items[uuid]["CheckWidgetNameField"])

        self.display_info(uuid)

        #Replaces Check Out Button in Item Info with Text Field (for name entry as well)
        self.info_panel_info["CheckWidgetButton"].deleteLater() #Removes the button
        self.info_panel_info["CheckWidgetNameField"] = QLineEdit()
        self.info_panel_info["CheckWidgetNameField"].setStyleSheet(qss.item_checkout_field)
        self.info_panel_info["CheckWidgetNameField"].setPlaceholderText("Enter Name...")
        self.info_panel_info["CheckWidgetNameField"].textChanged.connect(lambda: self.on_check_out_field_change(uuid, "InfoPanel"))
        self.info_panel_info["CheckWidgetNameField"].returnPressed.connect(lambda: self.complete_check_out(uuid))
        self.info_panel_info["CheckWidgetLayout"].addWidget(self.info_panel_info["CheckWidgetNameField"])

    def on_check_out_field_change(self, uuid:str, field:str):
        if field == "InfoPanel":
            self.rendered_items[uuid]["CheckWidgetNameField"].setText(self.info_panel_info["CheckWidgetNameField"].text())
        elif field == "Item":
            self.info_panel_info["CheckWidgetNameField"].setText(self.rendered_items[uuid]["CheckWidgetNameField"].text())

    def complete_check_out(self, uuid:str):
        modifications: dict[str, str] = {
            "availability": "Unavailable",
            "lastusedby": self.info_panel_info["CheckWidgetNameField"].text()
        }
        data_utils.modify_item_information(uuid, modifications)
        self.render_item_list()
        self.display_info(uuid)

    def display_info(self, uuid:str):
        item_info: dict = data_utils.get_item_information(uuid)
        for section in self.info_panel_info.values():
            try:
                section.deleteLater()
            except RuntimeError:
                continue
            except AttributeError:
                continue
        self.info_panel_info["name"] = QLabel(f"<h1>{item_info["name"]}</h1>")
        self.info_panel_info["name"].setStyleSheet(qss.no_qss)
        self.infopanellayout.insertWidget(0, self.info_panel_info["name"])

        self.info_panel_info["description"] = QLabel(item_info["description"])
        self.info_panel_info["description"].setStyleSheet(qss.no_qss)
        self.infopanellayout.insertWidget(1, self.info_panel_info["description"])

        self.info_panel_info["LastUsedByText"] = f"Item last checked out by: <b>{item_info['lastusedby']}</b>."
        self.info_panel_info["lastusedby"] = QLabel(self.info_panel_info["LastUsedByText"])
        self.info_panel_info["lastusedby"].setStyleSheet(qss.no_qss)
        self.infopanellayout.addWidget(self.info_panel_info["lastusedby"])

        self.info_panel_info["CheckWidget"] = QWidget()
        if item_info["is_available"] == "Available":
            self.info_panel_info["CheckWidgetButton"] = QPushButton("Check Out")
            self.info_panel_info["CheckWidgetButton"].setStyleSheet(qss.item_checkout_button)
            self.info_panel_info["CheckWidgetButton"].clicked.connect(lambda _: self.check_out(uuid))
        else:
            self.info_panel_info["CheckWidgetButton"] = QPushButton("Check In")
            self.info_panel_info["CheckWidgetButton"].setStyleSheet(qss.item_checkin_button)
            self.info_panel_info["CheckWidgetButton"].clicked.connect(lambda _: self.check_in(uuid))
        self.info_panel_info["CheckWidgetLayout"] = QHBoxLayout()
        self.info_panel_info["CheckWidgetLayout"].setContentsMargins(0, 0, 0, 0)
        self.info_panel_info["CheckWidgetLayout"].addWidget(self.info_panel_info["CheckWidgetButton"])
        self.info_panel_info["CheckWidget"].setLayout(self.info_panel_info["CheckWidgetLayout"])
        self.infopanellayout.addWidget(self.info_panel_info["CheckWidget"])

app = QApplication(sys.argv)
print("running...")

widget = MainWidget()
widget.show()

app.exec()
