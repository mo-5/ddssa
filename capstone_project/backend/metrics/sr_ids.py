from enum import Enum


class SrIds(Enum):
    """An enum used to represent the remediation to stall statements
    identified within source code. EXTRACT indicates that the stall
    statements should be moved outside of the loop, while delete
    indicates the statement should be completely removed from the
    source code as it serves no purpose in the code
    (i.e., frivolous operations)"""

    EXTRACT = 1
    DELETE = 2
