"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719,W0702
import json


def json_data_reader(_json, path: list[str], type: int) -> str:
    """
    -
    """
    data = None

    if type == 1:
        with open(_json, mode="r", encoding="utf-8") as file:
            data = json.load(file)
    elif type == 2:
        data = json.loads(_json)

    if len(path) == 1:
        return data[path[0]]

    if len(path) == 2:
        return data[path[0]][path[1]]

    if len(path) == 3:
        return data[path[0]][path[1]][path[2]]

    return data
