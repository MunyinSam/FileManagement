import os

source_dir = "C:/Users/Munyin/Downloads"

with os.scandir(source_dir) as entries:
    for entry in entries: #will run for each obj
        print(entry.name)
