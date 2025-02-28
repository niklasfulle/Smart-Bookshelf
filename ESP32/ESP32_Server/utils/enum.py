"""
-
"""


# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622
def enum(**enums):
    """
    -
    """
    return type("Enum", (), enums)
