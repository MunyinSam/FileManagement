import os
from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



# dest = destination
source_dir = "C:/Users/Munyin/Downloads"
dest_dir_sfx = "C:/Users/Munyin/Downloads/Sounds"
dest_dir_video = "C:/Users/Munyin/Downloads/Downloaded Video"
dest_dir_image = "C:/Users/Munyin/Downloads/Downloaded Images"
dest_dir_documents = "C:/Users/Munyin/Downloads/Documents"

document_list = [".doc", ".docx", ".odt",
                ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]


def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)

class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                dest = source_dir
                if name.endswith('.mp3') or name.endswith('.wav'):
                    dest = dest_dir_sfx
                    move(dest, entry, name)

                elif name.endswith('.mp4') or name.endswith('.mov'):
                    dest = dest_dir_video
                    move(dest, entry, name)
                
                elif name.endswith('.jpg') or name.endswith('.jpeg') or name.endswith('.png'):
                    dest = dest_dir_image
                    move(dest, entry, name)

                elif name.endswith in document_list:
                    dest = dest_dir_documents
                    move(dest, entry, name)

                




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()