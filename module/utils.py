import os
import json
from module import globalpy

def read_file(file_path):
    with open(file_path, "r") as f:
        json_data = json.load(f)
    return json_data

def check_json_exists():
    file_path = globalpy.GlobalVar.JSON_FILE_PATH
    dir_path = os.path.dirname(file_path)
    json_data = globalpy.GlobalVar.json_data

    # Create the dirs if dirs not exists
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)

    # Create the file if file not eixsts
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump(json_data, f, indent=4)

    return file_path

