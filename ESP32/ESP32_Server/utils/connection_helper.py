"""
-
"""


# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,W0719


def get_last_databuffer_element(databuffer: list, address):
    """
    Retrieves the index of the last element in the databuffer that matches the given address.

    Args:
        databuffer (list): A list of tuples or lists where the first element of each item is an address.
        address: The address to search for in the databuffer.

    Returns:
        int or None: The index of the last matching element if found, otherwise None.
    """

    result = next((i for i, v in enumerate(databuffer) if v[0] == address), None)
    return result
