#This file will contain functions to help manage data.

#Stardard Libraries
import csv
import uuid

#Third-Party Libraries

#Local Libraries

#File Names
item_csv: str = "local_data/items.csv"

def add_uuids_to_items():
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

def get_items(available_filter: bool|None = None) -> list[str]:
    """
    A function that returns the UUIDs of all the items that meet the filters,
    which are given as arguments to the function.
    If set to "None", then the filter is disregarded.
    e.g.
    """
    list_of_UUIDs: list[str] = []
    with open(item_csv, mode="r", newline="") as csv_file:
        read_file = list(csv.reader(csv_file))
        read_file.pop(0)
        for item in read_file:
            meets_availability_filter: bool|None = None
            if not available_filter is None:
                meets_availability_filter: bool|None = ((available_filter == True and item[1] == "Available") or
                                                        (available_filter == False and item[1] == "Unavailable"))
            if not meets_availability_filter == False:
                list_of_UUIDs.append(item[0])
    return list_of_UUIDs

def get_item_information(uuid:str) -> dict[str, str]:
    """
    A function that returns the basic information of an item, given the UUID.
    This currently gives the Name of the item & the item description,
    but will later give availability, number of issues, etc.
    """
    item_info: dict[str, str] = {}
    with open(item_csv, mode="r", newline="") as csv_file:
        read_file = list(csv.reader(csv_file))
        for item in read_file:
            if item[0] == uuid:
                item_info["name"] = item[2]
                item_info["description"] = item[3]
    return item_info

if __name__ == "__main__":
    print("Warning: File is intended to be used for utilities rather than run directly.")
    print("main.py is the intended file for this code to be ran from.")
    add_uuids_to_items()
    print(get_item_information("4e3d4cfc-1e45-42c3-8052-c3b356f12153"))
    print(get_items(True))
