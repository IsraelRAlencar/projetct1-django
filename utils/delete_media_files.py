import os
from pathlib import Path


def delete_files_in_folder(folder_path):
    try:
        if not os.path.isdir(folder_path):
            return

        files = os.listdir(folder_path)

        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

        delete_empty_folder(folder_path)
    except (ValueError, FileNotFoundError):
        ...


def delete_file(instance):
    try:
        os.remove(instance.cover.path)
        delete_empty_folder(Path(instance.cover.path).parent)
    except (ValueError, FileNotFoundError):
        ...


def delete_empty_folder(path):
    files = os.listdir(path)

    try:
        if len(files) == 0:
            os.rmdir(path)
    except (ValueError, FileNotFoundError):
        ...
