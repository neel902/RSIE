class USBAPI:
    def search():
        from pathlib import Path
        import os

        USBPath = Path(__file__).resolve().parent / "mount"
        return os.listdir(USBPath)

    class FileAPI:
        def __init__(self, usb):
            from pathlib import Path

            self.USBPath = Path(__file__).resolve().parent / "mount" / usb
        def format_drive(self):
            import json

            file_path = self.USBPath

            WELCOME = {"/": "Welcome to RASH's filesystem! This is the root directory. You can use the 'ls' command to list files and directories, 'cd <directory>' to change directories, and 'cat <file>' to view file contents."}

            with open(file_path, "w") as file:
                json.dump(WELCOME, file)

        def get_file(self, path):
            import json

            file_path = self.USBPath

            with open(file_path, "r") as file:
                content = json.load(file)

            return content.get(path, None) if path in content.keys() else "\033[91mUNKNOWN FILE\033[0m"

        def file_exists(self, path):
            import json

            file_path = self.USBPath

            with open(file_path, "r") as file:
                content = json.load(file)

            return path in content.keys()
        def set_file(self, path, value):
            import json

            file_path = self.USBPath

            with open(file_path, "r") as file:
                content = json.load(file)
            content[path] = value
            with open(file_path, "w") as file:
                json.dump(content, file)

        def delete_file(self, path):
            import json

            file_path = self.USBPath

            with open(file_path, "r") as file:
                content = json.load(file)
            if path in content:
                del content[path]
                with open(file_path, "w") as file:
                    json.dump(content, file)

        def list_files(self):
            import json

            file_path = self.USBPath

            with open(file_path, "r") as file:
                content = json.load(file)
            return list(content.keys())

        def list_file_regex(self, pattern):
            import json
            import re

            file_path = self.USBPath

            with open(file_path, "r") as file:
                content = json.load(file)
            return list((item for item in content.keys() if re.search(pattern, item)))

        def list_files_in_directory(self, directory):
            import json

            file_path = self.USBPath

            with open(file_path, "r") as file:
                content = json.load(file)
            return [key for key in content.keys() if key.startswith(directory) and ((key.count("/")) == (directory.count("/")) or (key.count("/")) == (directory.count("/")) + 1)]
        def drive_details(self, ):
            import json

            import os

            file_path = self.USBPath

            with open(file_path, "r") as file:
                content = json.load(file)
            return {
                "total_files": str(len(content)),
                "total_size": str(sum(len(value) for value in content.values())),
                "size_on_disk": f"{os.path.getsize(file_path)}B",
                "drive_name": str(os.path.basename(file_path)),
                "drive_format": "RASH-JSON-FS",
            }