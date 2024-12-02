from enum import Enum


class Role(str, Enum):
    NORMAL_USER = "NORMAL_USER"
    COLLECTOR= "COLLECTOR"

class WasteCategory(str, Enum):
    BIODEGRADABLE = "BIODEGRADABLE"
    NON_BIODEGRADABLE = "NON_BIODEGRADABLE"
    