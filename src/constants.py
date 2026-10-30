"""MindManager Constants and Enums."""

from enum import IntEnum
import re


def hex_to_argb(hex_color: str) -> tuple[int, int, int, int]:
    """Convert hex string (e.g. '#FF5733', '#11223344', or 'FF5733') to (A, R, G, B)."""
    clean = hex_color.strip().lstrip("#")
    if len(clean) == 6:
        r = int(clean[0:2], 16)
        g = int(clean[2:4], 16)
        b = int(clean[4:6], 16)
        return 255, r, g, b
    elif len(clean) == 8:
        a = int(clean[0:2], 16)
        r = int(clean[2:4], 16)
        g = int(clean[4:6], 16)
        b = int(clean[6:8], 16)
        return a, r, g, b
    elif len(clean) == 3:
        r = int(clean[0] * 2, 16)
        g = int(clean[1] * 2, 16)
        b = int(clean[2] * 2, 16)
        return 255, r, g, b
    else:
        # Default fallback to dark gray
        return 255, 60, 60, 60


class TopicShape(IntEnum):
    NONE = 1
    LINE = 2
    RECTANGLE = 3
    ROUNDED_RECTANGLE = 4
    HEXAGON = 5
    OCTAGON = 6
    CIRCLE = 7
    OVAL = 8
    IMAGE = 9
    DIAMOND = 10
    CAPSULE = 11
    DATA = 12
    DATABASE = 13
    PREDEFINED_PROCESS = 14
    DOCUMENT = 15


class BoundaryShape(IntEnum):
    LINES = 1
    ZIGZAG = 2
    SCALLOPS = 3
    WAVES = 4
    CURVED_LINE = 5
    RECTANGLE = 6
    CURVED_RECTANGLE = 7
    SUMMARY_ELBOW = 8
    SUMMARY_SHEARED_ELBOW = 9
    SUMMARY_ARC = 10
    SUMMARY_CURVE = 11


class LineDashStyle(IntEnum):
    SOLID = 1
    ROUND_DOT = 2
    SQUARE_DOT = 3
    DASH = 4
    DASH_DOT = 5
    LONG_DASH = 6
    LONG_DASH_DOT = 7
    LONG_DASH_DOT_DOT = 8


class TaskPriority(IntEnum):
    NONE = 0
    VERY_HIGH = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    VERY_LOW = 5
    PRIORITY_6 = 6
    PRIORITY_7 = 7
    PRIORITY_8 = 8
    PRIORITY_9 = 9


class StockIcon(IntEnum):
    UNKNOWN = 1
    SMILEY_HAPPY = 2
    SMILEY_NEUTRAL = 3
    SMILEY_SAD = 4
    SMILEY_ANGRY = 5
    SMILEY_SCREAMING = 6
    CLOCK = 7
    CALENDAR = 8
    LETTER = 9
    EMAIL = 10
    MAILBOX = 11
    MEGAPHONE = 12
    HOUSE = 13
    ROLODEX = 14
    DOLLAR = 15
    EURO = 16
    FLAG_RED = 17
    FLAG_BLUE = 18
    FLAG_GREEN = 19
    FLAG_BLACK = 20
    FLAG_ORANGE = 21
    FLAG_YELLOW = 22
    FLAG_PURPLE = 23
    TRAFFIC_LIGHTS_RED = 24
    MARKER_1 = 25
    MARKER_2 = 26
    MARKER_3 = 27
    MARKER_4 = 28
    MARKER_5 = 29
    MARKER_6 = 30
    MARKER_7 = 31
    RESOURCE_1 = 32
    RESOURCE_2 = 33
    PADLOCK_LOCKED = 34
    PADLOCK_UNLOCKED = 35
    ARROW_UP = 36
    ARROW_RIGHT = 37
    TWO_END_ARROW = 38
    PHONE = 39
    CELLPHONE = 40
    CAMERA = 41
    FAX = 42
    STOP = 43
    EXCLAMATION_MARK = 44
    QUESTION_MARK = 45
    THUMBS_UP = 46
    ON_HOLD = 47
    HOURGLASS = 48
    EMERGENCY = 49
    NO_ENTRY = 50
    BOMB = 51
    KEY = 52
    GLASSES = 53
    JUDGE_HAMMER = 54
    ROCKET = 55
    SCALES = 56
    REDO = 57
    LIGHTBULB = 58
    COFFEE_CUP = 59
    TWO_FEET = 60
    MEETING = 61
    CHECK = 62
    NOTE = 63
    THUMBS_DOWN = 64
    ARROW_LEFT = 65
    ARROW_DOWN = 66
    BOOK = 67
    MAGNIFYING_GLASS = 68
    BROKEN_CONNECTION = 69
    INFORMATION = 70
    FOLDER = 71
