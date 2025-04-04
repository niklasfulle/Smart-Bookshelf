"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719,W0702
import json


def json_data_reader(_json, path: list[str], type: int) -> str:
    """
    Reads and retrieves data from a JSON object or file based on a specified path.
    Args:
        _json (str): The JSON data as a string or the file path to a JSON file.
        path (list[str]): A list of keys representing the path to the desired data.
        type (int): Specifies the input type:
            - 1: `_json` is a file path to a JSON file.
            - 2: `_json` is a JSON string.
    Returns:
        str: The value retrieved from the JSON data at the specified path.
    Raises:
        KeyError: If the specified path does not exist in the JSON data.
        json.JSONDecodeError: If the JSON data is invalid.
        FileNotFoundError: If the file specified in `_json` does not exist (when type is 1).
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
