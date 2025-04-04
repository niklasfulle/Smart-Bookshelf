"""
-
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,C0103,W0719


class task:
    """
    Represents a task with associated metadata and data payload.
    Attributes:
        id (str): The unique identifier for the task.
        type (str): The type or category of the task.
        client_id (str): The identifier of the client associated with the task.
        data (str): The data or payload associated with the task.
    Methods:
        __init__(id: str, type: str, client_id: str, data: str) -> None:
            Initializes a new instance of the task class with the given attributes.
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
