import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
from pathlib import Path
from server import server
from flask import request, jsonify


@server.route('/notify', methods=['POST'])
def notify():
    uploaded_file = request.files['file']
    # Do something with the uploaded_file, like saving it
    # uploaded_file.save("path_to_save")
    return jsonify(success=True)


class Watcher:

    def __init__(self, directories_url: dict[str, str]):
        self.directories_url = directories_url
        self.observer = Observer()

    def run(self):
        event_handler = Handler(self.directories_url)

        # Schedule each directory with the observer
        for directory in self.directories_url.keys():
            self.observer.schedule(event_handler, directory, recursive=True)

        self.observer.start()
        try:
            while True:
                time.sleep(5)  # Check every 5 seconds
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):

    def __init__(self, directories_url):
        self.directories_url = directories_url

    def on_created(self, event):
        if event.is_directory:
            print(f"Directory created: {event.src_path}")
        else:
            print('FILE')
    # Notify the server or take other actions.


    def on_modified(self, event):
        if event.is_directory:
            return None


        elif event.event_type == 'created':
            # Event is created, you can process it now
            print("Watchdog received created event - % s." % event.src_path)

        elif event.event_type == 'modified':
            # Event is modified, you can process it now
            print("Watchdog received modified event - % s." % event.src_path)
            # Send the file to the server over HTTP
            file_path = event.src_path.replace('.part', '')
            f_path = Path(file_path)
            with open(file_path, 'rb') as f:
                server_url = self.directories_url[str(f_path.parent)]
                files = {'file': f}
                response = requests.post(server_url, files=files)
                print(response.text)


