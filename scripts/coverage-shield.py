import json
import sys
from enum import Enum


class Colors(str, Enum):
    BAD = "red"
    LOW = "orange"
    MEDIUM = "yellow"
    GOOD = "brightgreen"


def generate(tot):
    color = ""
    if int(tot) < 25:
        color = Colors.BAD
    if 25 < int(tot) < 50:
        color = Colors.LOW
    if 50 < int(tot) < 75:
        color = Colors.MEDIUM
    elif int(tot) > 75:
        color = Colors.GOOD

    print(json.dumps({
        "schemaVersion": 1,
        "label": "coverage",
        "message": f'{tot}%',
        "color": color
    }))


if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])
