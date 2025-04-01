"""
-
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103,W0719


class task:
    """_summary_

    Returns:
        _type_: _description_
    """

    id: str
    type: str
    client_id: str
    data: str

    def __init__(self, id: str, type: str, client_id: str, data: str) -> None:
        self.id = id
        self.type = type
        self.client_id = client_id
        self.data = data
