"""
    -
"""
import json

def json_data_reader(file_path, path: list[str]) -> str:
    """
        -
    """

    with open(file_path, mode = "r", encoding="utf-8") as file:
        data = json.load(file)

    print(data)

    return ""
