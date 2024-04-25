import os


def delete_files_in_folder(folder_path):
    if not os.path.isdir(folder_path):
        return

    files = os.listdir(folder_path)

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
