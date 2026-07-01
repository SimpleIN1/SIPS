
import glob
import os


import time
import psutil
import shutil
import logging
import fnmatch
import pathlib
from threading import Thread

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import conf
import utils.logger
from utils.mkdir import make_directory


make_directory(conf.PATH_FILE_TRACK_DIR)
make_directory(conf.PATH_FILE_TRACK_TMP_DIR)


class FileHandler(FileSystemEventHandler):

    def on_created(self, event):
        path = event.src_path

        logging.info(f"Add file {path}")

        file_size = -1
        while 1:
            current_size = os.path.getsize(path)
            if current_size == file_size:
                break
            file_size = current_size
            time.sleep(1)

        filename = os.path.basename(path)
        new_path = os.path.join(conf.PATH_FILE_TRACK_TMP_DIR, filename.replace(' ', '_'))
        shutil.copy2(path, new_path)
        os.remove(path)

        # Run algorithm

    def on_moved(self, event):
        print('Onmoved')


def run():
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, conf.PATH_FILE_TRACK_DIR, recursive=True)
    observer.start()

    while True:
        time.sleep(0.5)
