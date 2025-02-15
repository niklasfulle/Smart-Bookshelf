"""
    -
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R0914,C0103,R0902

class data_upload_package:
    """
        -
    """
    length: int
    message_type: bytearray
    data: any
    def __init__(
      self,
      length: bytearray,
      message_type: bytearray,
      data: any
    ) -> None:
        self.length = length
        self.message_type = message_type
        self.data = data
