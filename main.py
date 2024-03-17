import shutil, os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler
import send2trash

# Extensions for files
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp", ".svg"
                    , ".heif", ".heic", ".ico")                                # Modify Later

VIDEO_EXTENSIONS = (".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".mpg", ".mpeg"
                    , ".3gp")                                                  # Modify later

AUDIO_EXTENSIONS = (".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac")           # Modify later

DOCS_EXTENSIONS = (".csv", ".docx", ".pdf", ".py", ".ipynb", ".xlsx", ".txt")  # Modify later
# directories - modify these to make sure they match your directory
g_sourceDirectory = "C:/Users/some_name/Downloads"
g_imageDirectory = "C:/Users/some_name/Desktop/Images"
g_videoDirectory = "C:/Users/some_name/Desktop/Videos"
g_audioDirectory = "C:/Users/some_name/Desktop/Audio"
g_importantDocDirectory = "C:/Users/some_name/OneDrive/Desktop/SchoolDocuments"


def f_MoveFile(l_dest, l_entry, l_name):
    try:
        if DOCS_EXTENSIONS[0] in l_name:
            l_dest = "C:/Users/some_name/Desktop/SchoolDocuments/CSV Files"
        elif DOCS_EXTENSIONS[1] in l_name:
            l_dest = "C:/Users/some_name/Desktop/SchoolDocuments/DOCX Files"
        elif DOCS_EXTENSIONS[2] in l_name:
            l_dest = "C:/Users/some_name/Desktop/SchoolDocuments/PDF Files"
        elif DOCS_EXTENSIONS[3] in l_name:
            l_dest = "C:/Users/some_name/Desktop/SchoolDocuments/Python Files"
        elif DOCS_EXTENSIONS[4] in l_name:
            l_dest = "C:/Users/some_name/Desktop/SchoolDocuments/IPYNB Files"
        elif DOCS_EXTENSIONS[5] in l_name:
            l_dest = "C:/Users/some_name/Desktop/SchoolDocuments/XLSX Files"
        elif DOCS_EXTENSIONS[6] in l_name:
            l_dest = "C:/Users/some_name/Desktop/SchoolDocuments/Text Files"

        shutil.move(l_entry, l_dest)
    except shutil.Error:
        send2trash.send2trash(l_entry)


class MyEventHandler(FileSystemEventHandler):
    def on_modified(self, event: FileSystemEvent) -> None:
        with os.scandir(g_sourceDirectory) as m_entries:
            for m_entry in m_entries:
                m_name = m_entry.name
                m_dest = g_sourceDirectory

                for i in IMAGE_EXTENSIONS:
                    if i in m_name:
                        print(f"Image file {m_name} moved!")
                        f_MoveFile(g_imageDirectory, m_entry, m_name)

                for v in VIDEO_EXTENSIONS:
                    if v in m_name:
                        print(f"Video file {m_name} moved!")
                        f_MoveFile(g_videoDirectory, m_entry, m_name)

                for a in AUDIO_EXTENSIONS:
                    if a in m_name:
                        print(f"Audio file {m_name} moved!")
                        f_MoveFile(g_audioDirectory, m_entry, m_name)

                for id in DOCS_EXTENSIONS:
                    if id in m_name:
                        print(f"IMPORTANT FILE HAS BEEN MOVED! {m_name}")
                        f_MoveFile(g_importantDocDirectory, m_entry, m_name)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = g_sourceDirectory          # Modify to your exact path
    event_handler = MyEventHandler()  # Modify to your likening
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()