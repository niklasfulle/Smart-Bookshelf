"""
    -
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103,W0719

from ledstripe import ledstripe
class bookshelf:
    """_summary_

    Returns:
        _type_: _description_
    """
    name: str
    ip: str
    ledstripes: list[ledstripe]
    def __init__(
      self,
      name,
      ip,
      ledstrip_info
    ) -> None:
        self.name = name
        self.ip = ip
        self.ledstripes = []
