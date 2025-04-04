"""
-
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103,W0719


class ledstripe:
    """
    A class to represent an LED stripe.
    Attributes:
        order (int): The order or position of the LED stripe.
        length (int): The number of LEDs in the stripe.
    Methods:
        __init__(order, length):
            Initializes the LED stripe with the specified order and length.
    """

    order: int
    length: int

    def __init__(self, order, length) -> None:
        self.order = order
        self.length = length
