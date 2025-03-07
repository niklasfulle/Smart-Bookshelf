"""
    -
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719,W0702
import json

def json_data_reader(file_path, path: list[str]) -> str:
    """
        -
    """
    data = None

    with open(file_path, mode = "r", encoding="utf-8") as file:
        data = json.load(file)

    if len(path) == 1:
        return data[path[0]]

    if len(path) == 2:
        return data[path[0]][path[1]]

    if len(path) == 3:
        return data[path[0]][path[1]][path[2]]

    return data
