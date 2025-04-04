"""
-
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103,W0719

from hardware.ledstripe import ledstripe
from utils.constants import BOOKSHELF_MODE


class bookshelf:
    """
    Represents a bookshelf with associated LED stripes and operational mode.
    Attributes:
        name (str): The name of the bookshelf.
        ip (str): The IP address of the bookshelf.
        ledstripes (list[ledstripe]): A list of LED stripe objects associated with the bookshelf.
        mode (str): The current mode of the bookshelf, defaulting to BOOKSHELF_MODE.BOOKS.
    Methods:
        __init__(name: str, ip: str, ledstripe_data: list[dict]) -> None:
            Initializes a bookshelf instance with a name, IP address, and LED stripe data.
            Args:
                name (str): The name of the bookshelf.
                ip (str): The IP address of the bookshelf.
                ledstripe_data (list[dict]): A list of dictionaries containing LED stripe data,
                                             where each dictionary includes "order" and "length" keys.
    """

    name: str
    ip: str
    ledstripes: ledstripe
    mode: str

    def __init__(self, name: str, ip: str, ledstripe_data) -> None:
        """
        Initializes a Bookshelf instance.
        Args:
            name (str): The name of the bookshelf.
            ip (str): The IP address of the bookshelf.
            ledstripe_data (list): A list of dictionaries containing LED stripe data.
                Each dictionary should have the keys:
                    - "order" (int): The order of the LED stripe.
                    - "length" (int): The length of the LED stripe.
        Attributes:
            name (str): The name of the bookshelf.
            ip (str): The IP address of the bookshelf.
            ledstripes (list): A list of ledstripe objects initialized from the provided data.
            mode (BOOKSHELF_MODE): The current mode of the bookshelf, defaulting to BOOKSHELF_MODE.BOOKS.
        """

        self.name = name
        self.ip = ip
        self.ledstripes = []
        self.mode = BOOKSHELF_MODE.BOOKS

        for idx, ele in enumerate(ledstripe_data):
            self.ledstripes.insert(idx, ledstripe(ele["order"], ele["length"]))
