import os


def getParentPath(target_path):
    return os.path.abspath(os.path.join(target_path, os.pardir))
