"""
-
"""


# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719


def get_last_databuffer_element(databuffer: list, address):
    """
    -
    """
    result = next((i for i, v in enumerate(databuffer) if v[0] == address), None)
    return result
