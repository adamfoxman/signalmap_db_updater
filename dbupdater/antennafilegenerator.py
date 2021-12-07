from textwrap import wrap
from math import ceil, sqrt


def get_antenna_file(path: str,
                     antenna_filename: str,
                     antenna_direction: str,
                     pattern_h: str,
                     pattern_v: str):
    """
    Generates the antenna file for the given parameters.

    :param path: The path to the location file.
    :param external_id: The external id of a transmitter.
    :param transmitter_type: The type of the transmitter.
    :param country: The country of the location.
    :param antenna_direction: Information about the antenna direction.
    :param pattern_h: Horizontal pattern of an antenna.
    :param pattern_v: Vertical pattern of an antenna.
    :return: The antenna filename as a string.
    """
    if path[-1] != "/":
        path += "/"
    with open(f"{antenna_filename}.az", "w+") as antenna_file:
        pattern = []

        if pattern_h == "" and pattern_v == "" and antenna_direction != "":
            # to be implemented
            return None

        h_max_value, pattern_h = split_string_to_list(pattern_h)
        v_max_value, pattern_v = split_string_to_list(pattern_v)

        if pattern_h is not None and pattern_v is not None and len(pattern_h) == len(pattern_v):
            for i in range(len(pattern_h)):
                pattern.append(max(pattern_h[i], pattern_v[i]))
                max_value_dbw = max(h_max_value, v_max_value)
        elif pattern_h is not None and pattern_v is None:
            pattern = pattern_h
            max_value_dbw = h_max_value
        elif pattern_h is None and pattern_v is not None:
            pattern = pattern_v
            max_value_dbw = v_max_value
        else:
            return None

        max_value = sqrt((10 ** (max_value_dbw / 10)) * 75)

        antenna_file.write("0\n")

        for i in range(0, 360):
            left_side_value = float(pattern[ceil((i + 1) / 10) - 1 % 36])
            right_side_value = float(pattern[ceil((i + 1) / 10) % 36])
            value_dbw = float(
                right_side_value * (float(i) % 10.0) + left_side_value * (10.0 - (float(i) % 10.0))) / 10.0
            value = sqrt((10 ** (value_dbw / 10)) * 75) / max_value
            value = round(value, 6)
            antenna_file.write(str(i) + '\t' + str(value) + "\n")

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
        return max_value, pattern
