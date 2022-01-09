from enum import Enum


class PackageIds(Enum):
    """An enum used to represent the possible package information
    retrieved from different sources. Single indicates a SINGLE
    version number should be checked, RANGE indicates all versions
    between two version numbers should be checked, and MAX indicates
    that the version number provided up to the latest version number
    should be checked."""

    SINGLE = 1
    RANGE = 2
    MAX = 3
    NO_VER = 4
