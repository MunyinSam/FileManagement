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

image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
                    

video_extensions = [".webm", ".mpg",".mp4",".avi"]


audio_extensions = ["mp3", ".wav"]
# ? supported Document types
document_surnames = [".doc", ".docx", ".pdf",  ".ppt", ".pptx"]
                       


def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
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
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)

    def check_audio_files(self, entry, name): 
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) :
                
                dest = dest_dir_sfx
                move_file(dest, entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_video_files(self, entry, name): 
        for video_extension in video_extensions:
            if name.endswith(video_extension):
                move_file(dest_dir_video, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):  
        for image_extension in image_extensions:
            if name.endswith(image_extension):
                move_file(dest_dir_image, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_document_files(self, entry, name): 
        for documents_sur in document_surnames:
            if name.endswith(documents_sur):
                move_file(dest_dir_documents, entry, name)
                logging.info(f"Moved document file: {name}")

                




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler() # calls the whole class
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()