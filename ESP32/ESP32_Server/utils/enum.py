"""
-
"""


# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622
def enum(**enums):
    """
    Creates an enumeration type with the given keyword arguments.

    This function dynamically generates a simple enumeration class where the
    attributes and their values are defined by the provided keyword arguments.

    Example:
        Colors = enum(RED=1, GREEN=2, BLUE=3)
        print(Colors.RED)  # Output: 1

    Args:
        **enums: Arbitrary keyword arguments where the keys are the names of the
                 enumeration members and the values are their corresponding values.

    Returns:
        type: A dynamically created class with the specified attributes.
    """
    return type("Enum", (), enums)
