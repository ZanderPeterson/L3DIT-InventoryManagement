#This file will contain functions to help manage data.

#Stardard Libraries
import csv
import uuid

#Third-Party Libraries

#Local Libraries

#File Names
item_csv: str = "items.csv"

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

if __name__ == "__main__":
    print("Warning: File is intended to be used for utilities rather than run directly.")
    print("main.py is the intended file for this code to be ran from.")
    add_uuids_to_items()
