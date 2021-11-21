from textwrap import wrap
from math import ceil


def get_antenna_file(path: str,
                     id: int,
                     type: str,
                     country: str,
                     antenna_direction: str,
                     pattern_h: str,
                     pattern_v: str):
    if path[-1] != "/":
        path += "/"
    antenna_filename = f"{path}{country}_{type}_{id}.ant"
    try:
        antenna_file = open(antenna_filename, "w")
    except OSError:
        print(f"Can't open file {antenna_filename}")
        return

    h_max_value = 0
    v_max_value = 0
    pattern = []

    if pattern_h == "" and pattern_v == "" and antenna_direction != "":
        return None

    h_max_value, pattern_h = split_string_to_list(pattern_h)
    v_max_value, pattern_v = split_string_to_list(pattern_v)

    if pattern_h is not None and pattern_v is not None and len(pattern_h) == len(pattern_v):
        for i in range(len(pattern_h)):
            pattern.append(max(pattern_h[i], pattern_v[i]))
    elif pattern_h is not None and pattern_v is None:
        pattern = pattern_h
    elif pattern_h is None and pattern_v is not None:
        pattern = pattern_v

    for i in range(0, 360):
        left_side_value = int(pattern[ceil((i + 1) / 10) - 1 % 36])
        right_side_value = int(pattern[ceil((i + 1) / 10) % 36])
        value = (left_side_value * (i % 10) + right_side_value * (10 - (i % 10))) / 10
        antenna_file.write(str(value) + "\n")

    antenna_file.close()
    return antenna_filename

def split_string_to_list(pattern):
    if pattern == "":
        return 0, None
    else:
        pattern = wrap(pattern, 5)
        for line, string in enumerate(pattern):
            pattern[line] = float(string)
        max_value = max(pattern)
        for line, number in enumerate(pattern):
            pattern[line] = pattern[line] - max_value
        return max_value, pattern

