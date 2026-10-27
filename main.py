#This is the file that the user ought to execute.

#Standard Libraries
import sys #Required for opening a window

#Third-Party Libraries
#PySide6 Is the library used for all of my GUI Design.
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
                               QHBoxLayout, QVBoxLayout, QWidget, QSizePolicy,
                               QPlainTextEdit)

#Local Libraries
import qss #Used for styling all the elements
from local_data import data_utils #A python file used for handling data.

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Havelock North Scout Hall — Inventory Management") #Sets the title of the window
        self.resize(800, 600)
        data_utils.add_uuids_to_items() #If any new items are added, adds UUIDs to them

        #Layouts
        self.main_columns = QHBoxLayout()
        self.left_side = QVBoxLayout()
        self.right_side = QVBoxLayout()

        #Set up title
        self.title_label = QLabel("<h1>Inventory Management</h1>") #Creates a heading for the output section
        self.title_label.setStyleSheet(qss.basic_element)
        self.left_side.addWidget(self.title_label, alignment=Qt.AlignCenter)

        #Set up Search & Filtering
        self.search_layout = QHBoxLayout()
        self.search_icon = QLabel()
        self.search_icon.setStyleSheet(qss.search_icon)
        self.search_layout.addWidget(self.search_icon)

        self.search_bar = QLineEdit()
        self.search_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.search_bar.setStyleSheet(qss.basic_element)
        self.search_bar.setPlaceholderText("Enter your search...")
        #The following line updates the list of items displayed whenever the
        #search bar is updated.
        self.search_bar.textChanged.connect(lambda _: self.render_item_list())
        self.search_layout.addWidget(self.search_bar)
        self.right_side.addLayout(self.search_layout)

        #Set up the inventory available/unavailable buttons
        self.available_inventory_filter_layout = QHBoxLayout()
        self.available_inventory_filter_label = QLabel("Sort By:")
        self.available_inventory_filter_label.setStyleSheet(qss.basic_element)
        self.available_inventory_filter_layout.addWidget(self.available_inventory_filter_label, stretch=2)
        self.show_available_inventory: bool = True #True = available inventory, False = unavailable inventory.

        self.available_inventory_button = QPushButton("Inventory Available")
        self.available_inventory_button.setStyleSheet(qss.inventory_available_button_style)
        self.available_inventory_button.clicked.connect(lambda: self.available_inventory_filter(True))
        self.available_inventory_button.setCheckable(True)
        self.available_inventory_filter_layout.addWidget(self.available_inventory_button, stretch=3)

        self.unavailable_inventory_button = QPushButton("Inventory Unavailable")
        self.unavailable_inventory_button.setStyleSheet(qss.inventory_unavailable_button_style)
        self.unavailable_inventory_button.clicked.connect(lambda: self.available_inventory_filter(False))
        self.unavailable_inventory_button.setCheckable(True)
        self.available_inventory_filter_layout.addWidget(self.unavailable_inventory_button, stretch=3)

        self.right_side.addLayout(self.available_inventory_filter_layout)

        #Set up the issue filter buttons
        self.issue_filter_layout = QHBoxLayout()
        self.issue_filter_label = QLabel("Sort By:")
        self.issue_filter_label.setStyleSheet(qss.basic_element)
        self.issue_filter_layout.addWidget(self.issue_filter_label, stretch=1)
        self.show_issues: bool|None = False #False = NoIssues, True = Issues, None = Show All

        self.noissues_filter_button = QPushButton("No Issues")
        self.noissues_filter_button.setStyleSheet(qss.noissues_button_style)
        self.noissues_filter_button.setCheckable(True)
        self.noissues_filter_button.clicked.connect(lambda: self.issues_filter(False))
        self.issue_filter_layout.addWidget(self.noissues_filter_button, stretch=1)

        self.issues_filter_button = QPushButton("Issues")
        self.issues_filter_button.setStyleSheet(qss.issues_button_style)
        self.issues_filter_button.setCheckable(True)
        self.issues_filter_button.clicked.connect(lambda: self.issues_filter(True))
        self.issue_filter_layout.addWidget(self.issues_filter_button, stretch=1)

        self.all_filter_button = QPushButton("All")
        self.all_filter_button.setStyleSheet(qss.all_button_style)
        self.all_filter_button.setCheckable(True)
        self.all_filter_button.clicked.connect(lambda: self.issues_filter(None))
        self.issue_filter_layout.addWidget(self.all_filter_button, stretch=1)

        self.right_side.addLayout(self.issue_filter_layout)

        #Display List o' Items
        self.item_list_widget = QWidget()
        self.item_list_widget.setStyleSheet(qss.item_list_available)
        self.item_list_layout = QVBoxLayout()
        self.item_list_widget.setLayout(self.item_list_layout)
        self.rendered_items: dict[str, dict[QWidget]] = {}
        self.no_items_popup = QLabel("No items matched your search")
        self.no_items_popup.setStyleSheet(qss.basic_element)
        self.no_items_popup.setVisible(False)
        self.item_list_layout.addWidget(self.no_items_popup)
        self.item_list_layout.addStretch()
        self.add_item = QLineEdit()
        self.add_item.setStyleSheet(qss.basic_element)
        self.add_item.setPlaceholderText("Enter new item...")
        self.add_item.returnPressed.connect((lambda: self.add_new_item()))
        self.item_list_layout.addWidget(self.add_item)
        self.right_side.addWidget(self.item_list_widget)

        #Display the Info Panel
        self.info_panel_widget = QWidget()
        self.info_panel_widget.setStyleSheet(qss.basic_element)
        self.info_panel_widget.setContentsMargins(12, 12, 12, 12)
        self.info_panel_layout = QVBoxLayout()
        self.info_panel_widget.setLayout(self.info_panel_layout)
        self.info_panel_info: dict[str, dict[QWidget]] = {}
        self.info_panel_issues: list[dict[QWidget]] = []
        self.info_panel_description: str = ""
        self.info_panel_layout.addStretch()
        self.currently_viewed_uuid: str | None = None
        self.left_side.addWidget(self.info_panel_widget)

        #Adds both of the sides to the overall layout
        #The stretch encourages both sides to have the same width.
        self.main_columns.addLayout(self.left_side, stretch=1)
        self.main_columns.addLayout(self.right_side, stretch=1)

        #Sets the default states of buttons
        self.available_inventory_filter(self.show_available_inventory)
        self.issues_filter(self.show_issues) #Ensures one option is selected initially

        self.setLayout(self.main_columns) #Displays layout

    def render_item_list(self) -> None:
        """Renders all items in the item list, as per filters"""
        self.display_info() #Updates the InfoPanel

        #This clears whatever was previously rendered
        for item in self.rendered_items.values():
            item["QWidget"].deleteLater()
        self.rendered_items = {}

        items: List[str] = data_utils.get_items(self.show_available_inventory, self.show_issues, self.search_bar.text())
        self.no_items_popup.setText("Unfortunately, No items matched with your search & filters")
        self.no_items_popup.setVisible(len(items) == 0) #Shows the "no items" popup if no items are found
        for item_uuid in items:
            self.rendered_items[item_uuid] = {}
            self.rendered_items[item_uuid]["QWidget"] = QWidget()
            self.rendered_items[item_uuid]["QWidget"].setStyleSheet(qss.item_in_list)
            self.rendered_items[item_uuid]["Layout"] = QHBoxLayout()
            self.rendered_items[item_uuid]["Layout"].setContentsMargins(10, 0, 0, 0)

            self.rendered_items[item_uuid]["ButtonLabel"] = QPushButton(data_utils.get_item_information(item_uuid)["Name"])
            self.rendered_items[item_uuid]["ButtonLabel"].setStyleSheet(qss.item_label)
            self.rendered_items[item_uuid]["ButtonLabel"].clicked.connect(lambda _, uuid=item_uuid: self.display_info(uuid))
            self.rendered_items[item_uuid]["Layout"].addWidget(self.rendered_items[item_uuid]["ButtonLabel"], stretch=2)

            number_of_issues: int = len(data_utils.get_item_information(item_uuid)["Issues"])
            issues_message: str = f"Issues: {number_of_issues}"
            self.rendered_items[item_uuid]["IssuesNumber"] = QPushButton(issues_message)
            self.rendered_items[item_uuid]["IssuesNumber"].clicked.connect(lambda _, uuid=item_uuid: self.display_info(uuid))
            if number_of_issues >= 1:
                self.rendered_items[item_uuid]["IssuesNumber"].setStyleSheet(qss.item_has_issues)
            else:
                self.rendered_items[item_uuid]["IssuesNumber"].setStyleSheet(qss.item_has_no_issues)
            self.rendered_items[item_uuid]["Layout"].addWidget(self.rendered_items[item_uuid]["IssuesNumber"])

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
            insert_widget_location = max(0, self.item_list_layout.count()-2) #Ensures widget is before stretch
            self.item_list_layout.insertWidget(insert_widget_location, self.rendered_items[item_uuid]["QWidget"])

    def available_inventory_filter(self, available_inventory_button_pressed: bool) -> None:
        """
        Should be called when the availability inventory filter is being changed.
        This function also updates the item list.
        """
        self.show_available_inventory = available_inventory_button_pressed

        #Sets the Available & Unavailable Filter Buttons to be properly checked.
        self.available_inventory_button.setChecked(self.show_available_inventory)
        self.unavailable_inventory_button.setChecked(not self.show_available_inventory)

        #Sets the colour of the itemlist to be Green or Red, dependent on if
        #Available items is selected or Unavailable items are selected
        if self.show_available_inventory:
            self.item_list_widget.setStyleSheet(qss.item_list_available)
        else:
            self.item_list_widget.setStyleSheet(qss.item_list_unavailable)
        self.render_item_list() #Updates the item list to apply filters.

    def issues_filter(self, issues_filter_pressed: bool|None) -> None:
        """
        Should be called when the issues filter is being changed.
        This function also updates the item list.
        """
        self.show_issues = issues_filter_pressed
        self.noissues_filter_button.setChecked(self.show_issues == False)
        self.issues_filter_button.setChecked(self.show_issues == True)
        self.all_filter_button.setChecked(self.show_issues is None)
        self.render_item_list()

    def check_in(self, uuid:str) -> None:
        """Called when checking in an item. Also updates the item list."""
        data_utils.modify_item_information(uuid, {"Availability": "Available"})
        self.render_item_list() #Updates the item list to apply filters.

    def check_out(self, uuid:str) -> None:
        """Called when checking out an item. Also updates the Display Panel."""
        self.display_info(uuid)  # Updates the InfoPanel

        #Replaces Check Out Button on Item with Text Field (for name entry)
        self.rendered_items[uuid]["CheckWidgetButton"].deleteLater() #Removes the button
        self.rendered_items[uuid]["CheckWidgetNameField"] = QLineEdit()
        self.rendered_items[uuid]["CheckWidgetNameField"].setStyleSheet(qss.item_checkout_field)
        self.rendered_items[uuid]["CheckWidgetNameField"].setPlaceholderText("Enter Name...")
        self.rendered_items[uuid]["CheckWidgetNameField"].textChanged.connect(lambda: self.on_check_out_field_change(uuid, "Item"))
        self.rendered_items[uuid]["CheckWidgetNameField"].returnPressed.connect(lambda: self.complete_check_out(uuid))
        self.rendered_items[uuid]["CheckWidgetLayout"].addWidget(self.rendered_items[uuid]["CheckWidgetNameField"])
        #This line makes sure the CheckWidgetNameField is focussed, but in order
        #to do so, the CheckWidgetNameField must have been rendered. So, this
        #will schedule focussing CheckWidgetNameField for whenever rendering
        #has been completed, allowing for reliable behaviour.
        QTimer.singleShot(0, self.rendered_items[uuid]["CheckWidgetNameField"].setFocus)

        #Replaces Check Out Button in Item Info with Text Field (for name entry as well)
        self.info_panel_info["CheckWidgetButton"].deleteLater() #Removes the button
        self.info_panel_info["CheckWidgetNameField"] = QLineEdit()
        self.info_panel_info["CheckWidgetNameField"].setStyleSheet(qss.item_checkout_field)
        self.info_panel_info["CheckWidgetNameField"].setPlaceholderText("Enter Name...")
        self.info_panel_info["CheckWidgetNameField"].textChanged.connect(lambda: self.on_check_out_field_change(uuid, "InfoPanel"))
        self.info_panel_info["CheckWidgetNameField"].returnPressed.connect(lambda: self.complete_check_out(uuid))
        self.info_panel_info["CheckWidgetLayout"].addWidget(self.info_panel_info["CheckWidgetNameField"])

    def on_check_out_field_change(self, uuid:str, field:str) -> None:
        """
        Keeps the two check out buttons synchronised.
        Should be called whenever either text field is updated
        """
        if field == "InfoPanel":
            self.rendered_items[uuid]["CheckWidgetNameField"].setText(self.info_panel_info["CheckWidgetNameField"].text())
        elif field == "Item":
            self.info_panel_info["CheckWidgetNameField"].setText(self.rendered_items[uuid]["CheckWidgetNameField"].text())

    def complete_check_out(self, uuid:str) -> None:
        """
        Should be called when a check-out is being completed.
        Also updates the item list.
        """
        modifications: dict[str, str] = {
            "Availability": "Unavailable",
            "LastUsedBy": self.info_panel_info["CheckWidgetNameField"].text()
        }
        data_utils.modify_item_information(uuid, modifications)
        self.render_item_list()

    def display_info(self, uuid:str|None = None) -> None:
        """Responsible for rendering the Info Panel."""
        #This clears whatever was previously rendered
        for issue in self.info_panel_issues:
            try:
                issue.deleteLater()
            except RuntimeError:
                continue
            except AttributeError:
                continue
        for section in self.info_panel_info.values():
            try:
                section.deleteLater()
            except RuntimeError:
                continue
            except AttributeError:
                continue

        if uuid is None and self.currently_viewed_uuid is None:
            return #If no uuid has been entered by the user, then display nothing.
        if not self.currently_viewed_uuid is None:
            #If there was an item previously being displayed in the InfoPanel,
            #Then this code ensures the description (which may have been
            #edited) has been properly saved.
            self.update_item_description(self.currently_viewed_uuid, True)
        if uuid is None:
            uuid = self.currently_viewed_uuid
        self.currently_viewed_uuid = uuid
        item_info: dict = data_utils.get_item_information(uuid)

        self.info_panel_info["Name"] = QLabel(f"<h1>{item_info["Name"]}</h1>")
        self.info_panel_info["Name"].setStyleSheet(qss.no_qss)
        self.info_panel_layout.insertWidget(0, self.info_panel_info["Name"])

        #Using a QPlainTextEdit to allow for the description to be edited.
        #A QLabel does not allow editing, and the usual QLineEdit is only
        #for single line entries only (whereas this may be multiline)
        self.info_panel_info["Description"] = QPlainTextEdit()
        self.info_panel_info["Description"].setStyleSheet(qss.no_qss)
        self.info_panel_info["Description"].setPlaceholderText("Add a description...")
        self.info_panel_info["Description"].setPlainText(item_info["Description"])
        self.info_panel_info["Description"].textChanged.connect(lambda: self.update_item_description(uuid, False))
        self.update_item_description(uuid, False)
        self.info_panel_layout.insertWidget(1, self.info_panel_info["Description"])

        self.info_panel_info["Issues"] = QWidget()
        self.info_panel_info["IssuesLayout"] = QVBoxLayout()
        if len(item_info["Issues"]) == 0:
            self.info_panel_info["Issues"].setStyleSheet(qss.item_has_no_issues)
            self.info_panel_issues = [{"NoIssuesMessage": QLabel("There are no reported issues on this item")}]
            self.info_panel_issues[0]["NoIssuesMessage"].setStyleSheet(qss.basic_element)
            self.info_panel_info["IssuesLayout"].addWidget(self.info_panel_issues[0]["NoIssuesMessage"])
        else:
            self.info_panel_info["Issues"].setStyleSheet(qss.item_has_issues)
            for issue in item_info["Issues"]:
                self.info_panel_issues.append({"QWidget": QWidget(),
                                               "Layout": QHBoxLayout(),
                                               "IssueText": QLabel(issue),
                                               "DeleteButton": QPushButton("Mark Resolved")})
                self.info_panel_issues[-1]["Layout"].setContentsMargins(0, 0, 0, 0)
                self.info_panel_issues[-1]["QWidget"].setStyleSheet(qss.basic_element)

                self.info_panel_issues[-1]["IssueText"].setStyleSheet(qss.item_label)
                self.info_panel_issues[-1]["Layout"].addWidget(self.info_panel_issues[-1]["IssueText"], stretch=2)

                self.info_panel_issues[-1]["DeleteButton"].setStyleSheet(qss.noissues_button_style)
                self.info_panel_issues[-1]["DeleteButton"].clicked.connect(lambda: self.delete_issue(uuid, issue))
                self.info_panel_issues[-1]["Layout"].addWidget(self.info_panel_issues[-1]["DeleteButton"], stretch=1)

                self.info_panel_issues[-1]["QWidget"].setLayout(self.info_panel_issues[-1]["Layout"])
                self.info_panel_info["IssuesLayout"].addWidget(self.info_panel_issues[-1]["QWidget"])

        self.info_panel_info["AddIssue"] = QLineEdit()
        self.info_panel_info["AddIssue"].setStyleSheet(qss.basic_element)
        self.info_panel_info["AddIssue"].setPlaceholderText("Enter new issue...")
        self.info_panel_info["AddIssue"].returnPressed.connect((lambda: self.add_new_issue(uuid)))
        self.info_panel_info["IssuesLayout"].addWidget(self.info_panel_info["AddIssue"])

        self.info_panel_info["Issues"].setLayout(self.info_panel_info["IssuesLayout"])
        self.info_panel_layout.insertWidget(2, self.info_panel_info["Issues"])

        self.info_panel_info["LastUsedByText"] = f"Item last checked out by: <b>{item_info["LastUsedBy"]}</b>."
        self.info_panel_info["LastUsedBy"] = QLabel(self.info_panel_info["LastUsedByText"])
        self.info_panel_info["LastUsedBy"].setStyleSheet(qss.no_qss)
        self.info_panel_layout.addWidget(self.info_panel_info["LastUsedBy"])

        self.info_panel_info["CheckWidget"] = QWidget()
        #If item is Available, show Check Out Button.
        #Otherwise, show Check In Button.
        if item_info["IsAvailable"] == "Available":
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
        self.info_panel_layout.addWidget(self.info_panel_info["CheckWidget"])

        self.info_panel_info["BottomRow"] = QHBoxLayout()
        self.info_panel_info["DeleteItem"] = QPushButton("Delete Item")
        self.info_panel_info["DeleteItem"].setStyleSheet(qss.inventory_unavailable_button_style)
        self.info_panel_info["DeleteItem"].clicked.connect(lambda _: self.delete_item(uuid))
        self.info_panel_info["BottomRow"].addWidget(self.info_panel_info["DeleteItem"])

        self.info_panel_info["GenerateLog"] = QPushButton("Generate Log")
        self.info_panel_info["GenerateLog"].setStyleSheet(qss.inventory_available_button_style)
        self.info_panel_info["GenerateLog"].clicked.connect(lambda _: data_utils.generate_log_file(uuid, "generated_logs"))
        self.info_panel_info["BottomRow"].addWidget(self.info_panel_info["GenerateLog"])
        self.info_panel_layout.addLayout(self.info_panel_info["BottomRow"])

    def add_new_item(self) -> None:
        """Called when adding a new item. Also updates the item list."""
        name: str = self.add_item.text()
        data_utils.add_new_item(name)
        self.render_item_list()

    def update_item_description(self, uuid:str, commit:bool) -> None:
        """
        Called when updating an item description.
        If commit is False, it saves the current description to a variable
        (This allows the description to still be known, even if the QTextEdit
        were to be removed due to the user switching items).
        If commit is True, the edited description gets saved.
        commit should not be True all the time. Otherwise, the log would fill
        with every single character being edited (as well as being inefficient)
        """
        if not commit:
            self.info_panel_description = self.info_panel_info["Description"].toPlainText()
            return
        data_utils.modify_item_information(uuid, {"Description": self.info_panel_description})

    def delete_item(self, uuid:str) -> None:
        """Called when deleting an item. Also updates the item list."""
        data_utils.delete_item(uuid)
        self.currently_viewed_uuid = None
        self.render_item_list()

    def add_new_issue(self, uuid:str) -> None:
        """Called when adding an issue. Also updates the item list."""
        issue: str = self.info_panel_info["AddIssue"].text()
        data_utils.add_new_issue(uuid, issue)
        self.render_item_list()

    def delete_issue(self, uuid:str, issue:str) -> None:
        """Called when removing an issue. Also updates the item list."""
        data_utils.remove_issue(uuid, issue)
        self.render_item_list()

app = QApplication(sys.argv)
print("running...")

widget = MainWidget()
widget.show()

app.exec()
