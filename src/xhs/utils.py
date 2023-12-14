import os
import json

def get_base_folder():
    dir = os.path.dirname(os.path.realpath(__file__))
    dir = os.path.dirname(dir)
    dir = os.path.dirname(dir)
    return dir


def get_statics_folder():
    base_dir = get_base_folder()
    return os.path.join(base_dir, "statics")


def beauty_print(data: dict):
    print(json.dumps(data, ensure_ascii=False, indent=2))
