import os

def separate_folder_tree(path, level):
    subfolders = []

    path = os.path.normpath(path)
    root_depth = path.count(os.sep)

    for dirpath, dirnames, filenames in os.walk(path):
        depth = dirpath.count(os.sep) - root_depth
        if depth == level:
            subfolders.append(dirpath)

    return subfolders

def get_file_paths(directory):
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_paths.append(file_path)
    return file_paths
