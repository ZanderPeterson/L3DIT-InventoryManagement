#This file will contain functions to help manage data.

#Stardard Libraries
import csv
from datetime import datetime
import uuid

#Third-Party Libraries

#Local Libraries

#File Names
item_csv: str = "local_data/items.csv"
issues_csv: str = "local_data/issues.csv"
log_csv: str = "local_data/log.csv"

def add_uuids_to_items() -> None:
    """
    Checks through items.csv and finds any missing UUIDs (These may be present
    if the user has just manually added new rows). If missing UUIDs are found,
    the empty cells are replaced with newly generated UUIDs (using uuid.uuid4)
    """
    with open(item_csv, mode="r", newline="") as csv_file:
        read_file = list(csv.reader(csv_file))
        for row in read_file:
            if row[0] == '':
                row[0] = uuid.uuid4() #Adds a UUID, if no UUID is present
                print(f"Added UUID to {row}")

    with open(item_csv, mode="w", newline="") as csv_file:
        csv.writer(csv_file).writerows(read_file) #Writes file w/changes.

def add_to_log(uuid:str, change:str) -> None:
    """Adds specified information to the log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_csv, mode="a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([uuid, timestamp, change])

def generate_log_file(uuid:str, directory:str) -> None:
    """
    Generates a .txt file which shows the full history of the item.
    The directory variable refers to the location the file should be generated.
    """
    item_info: dict[str, str] = get_item_information(uuid)
    file_name: str = f"{directory}/{item_info["name"]} Log.txt"
    add_to_log(uuid, f"Generated Log File: {file_name}")

    #Reads log file
    with open(log_csv, mode="r", newline="") as csv_file:
        read_file = list(csv.reader(csv_file))

    #Keeps only the relevant logged lines, and formats lines.
    info_to_write: list[str] = []
    for entry in read_file:
        if entry[0] != uuid:
            continue
        info_to_write.append(f"[{entry[1]}]: {entry[2]}\n")

    #Writes the log file.
    with open(file_name, mode="w", encoding="utf-8") as log_file:
        log_file.write(f"This is the log file for {item_info["name"]}\n")
        log_file.write(f"This file was generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n")
        log_file.writelines(info_to_write)

def get_items(available_filter: bool|None = None,
              issues_filter: bool|None = None,
              search: str|None = None) -> list[str]:
    """
    A function that returns the UUIDs of all the items that meet the filters,
    which are given as arguments to the function.
    If set to "None", then the filter is disregarded.
    """
    valid_uuids: list[str] = []
    with (open(item_csv, mode="r", newline="") as csv_file):
        read_file = list(csv.reader(csv_file))
        read_file.pop(0)
        if not search is None:
            search = search.replace(" ", "").lower()
            if search == "":
                search = None
            print(f"new search: {search}")
        for item in read_file:
            meets_availability_filter: bool|None = None
            meets_issues_filter: bool|None = None
            meets_search_filter: bool|None = None
            item_information: dict[str, str] = get_item_information(item[0])
            if not available_filter is None:
                meets_availability_filter = ((available_filter == True and item_information["IsAvailable"] == "Available") or
                                             (available_filter == False and item_information["IsAvailable"] == "Unavailable"))
            if not issues_filter is None:
                meets_issues_filter = ((issues_filter == True and len(item_information["Issues"]) >= 1) or
                                       (issues_filter == False and len(item_information["Issues"]) == 0))
            if not search is None:
                to_search: str = item_information["name"]+item_information["description"]
                meets_search_filter = search in (to_search).replace(" ", "").lower()
            if ((not meets_availability_filter == False) and
                (not meets_issues_filter == False) and
                (not meets_search_filter == False)):
                valid_uuids.append(item[0])
    return valid_uuids

def get_item_information(uuid:str) -> dict[str, str]:
    """
    A function that returns the basic information of an item, given the UUID.
    This currently gives the Name of the item & the item description,
    availability, and a list of issues.
    The dictionary has the following keys & values:
    ['Issues'] —> A string containing an array of strings with have the item's
                  issues. If no issues are found, this array will be empty.
    ['IsAvailable'] —> Should either be 'Available' or 'Unavailable'
    ['Name'] —> A string containing the item's name.
    ['Description'] —> A string containing the item's description
    ['LastUsedBy'] —> A string containing the name of the item's last user.
    """
    item_info: dict[str, str] = {"Issues": []}
    with open(item_csv, mode="r", newline="") as csv_file:
        read_file = list(csv.reader(csv_file))
        for item in read_file:
            if item[0] == uuid:
                item_info["IsAvailable"] = item[1]
                item_info["Name"] = item[2]
                item_info["Description"] = item[3]
                item_info["LastUsedBy"] = item[4]
    with open(issues_csv, mode="r", newline="") as csv_file:
        read_file = list(csv.reader(csv_file))
        for item in read_file:
            if item[0] == uuid:
                item_info["Issues"].append(item[1])
    return item_info

def modify_item_information(uuid:str, modifications: dict[str, str]):
    """
    Modifies existing item information using a dictionary.
    The keys and values of the dictionary are the same as
    get_item_information(), and are as follows:
    ['Issues'] —> A string containing an array of strings with have the item's
                  issues. If no issues are found, this array will be empty.
    ['IsAvailable'] —> Should either be 'Available' or 'Unavailable'
    ['Name'] —> A string containing the item's name.
    ['Description'] —> A string containing the item's description
    ['LastUsedBy'] —> A string containing the name of the item's last user.
    If these result in values changes, they are logged.
    """
    with open(item_csv, mode="r", newline="") as csv_file:
        read_file = list(csv.reader(csv_file))

    for row in read_file:
        if row[0] != uuid:
            continue
        try:
            row[1] = modifications["Availability"]
            if modifications["Availability"] == "Available":
                add_to_log(uuid, f"Item Checked In")
            if modifications["Availability"] == "Unavailable":
                add_to_log(uuid, f"Item Checked Out by: {modifications["LastUsedBy"]}")
        except KeyError:
            pass

        try:
            row[2] = modifications["Name"]
        except KeyError:
            pass

        try:
            if row[3] != modifications["Description"]:
                add_to_log(uuid, f"Updated Description To: {modifications["description"]}")
                row[3] = modifications["Description"]
        except KeyError:
            pass

        try:
            row[4] = modifications["LastUsedBy"]
        except KeyError:
            pass

    with open(item_csv, mode="w", newline="") as csv_file:
        csv.writer(csv_file).writerows(read_file)

def add_new_item(item_name:str) -> None:
    """Adds a new item, and logs it."""
    new_uuid: str = str(uuid.uuid4())
    add_to_log(new_uuid, f"Added Item: {item_name}")
    with open(item_csv, mode="a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([new_uuid, "Available", item_name, "", "Never Checked Out"])

def delete_item(uuid:str) -> None:
    """Deletes an existing item, and logs it."""
    add_to_log(uuid, "Deleted Item")
    with open(item_csv, mode="r", newline="") as csv_file:
        read_file = list(csv.reader(csv_file))
        new_file = []
        for row in read_file:
            if row[0] == uuid:
                break
            else:
                new_file.append(row)
    with open(item_csv, mode="w", newline="") as csv_file:
        csv.writer(csv_file).writerows(new_file)

def add_new_issue(uuid:str, issue:str) -> None:
    """Adds a new issue, and logs it."""
    add_to_log(uuid, f"Added issue: {issue}")
    with open(issues_csv, mode="a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([uuid, issue])

def remove_issue(uuid:str, issue:str) -> None:
    """Deletes an issue, and logs it."""
    add_to_log(uuid, f"Removed issue: {issue}")
    with open(issues_csv, mode="r", newline="") as csv_file:
        read_file = list(csv.reader(csv_file))
        new_file = []
        for row in read_file:
            if row[0] == uuid and row[1] == issue:
                break
            else:
                new_file.append(row)
    with open(issues_csv, mode="w", newline="") as csv_file:
        csv.writer(csv_file).writerows(new_file)

if __name__ == "__main__":
    #This was useful for development, but is not intended to ever be seen by the user.
    print("Warning: File is intended to be used for utilities rather than run directly.")
    print("main.py is the intended file for this code to be ran from.")
    add_uuids_to_items()
    print(get_item_information("4e3d4cfc-1e45-42c3-8052-c3b356f12153"))
    #print(get_items(True))
    modify_item_information("c08e9b7e-fd60-417d-a7fe-d80346bd8614", {"Availability": "Available"})
