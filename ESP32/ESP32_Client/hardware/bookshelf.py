"""
-
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103,W0719

from hardware.ledstripe import ledstripe
from utils.constants import BOOKSHELF_MODE


class bookshelf:
    """_summary_

    Returns:
        _type_: _description_
    """

    name: str
    ip: str
    ledstripes: ledstripe
    mode: str

    def __init__(self, name: str, ip: str, ledstripe_data) -> None:
        self.name = name
        self.ip = ip
        self.ledstripes = []
        self.mode = BOOKSHELF_MODE.BOOKS

        for idx, ele in enumerate(ledstripe_data):
            self.ledstripes.insert(idx, ledstripe(ele["order"], ele["length"]))
