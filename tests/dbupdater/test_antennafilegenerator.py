from dbupdater.antennafilegenerator import parse_antenna_direction, split_string_to_list, get_antenna_file


def test_parse_antenna_direction():
    assert parse_antenna_direction("0") == [{"beam": 0}]
    assert parse_antenna_direction("90") == [{"beam": 90}]
    assert parse_antenna_direction("180") == [{"beam": 180}]
    assert parse_antenna_direction("0,90,180") == [{"beam": 0}, {"beam": 90}, {"beam": 180}]
    assert parse_antenna_direction("0,90,180,270") == [{"beam": 0}, {"beam": 90}, {"beam": 180}, {"beam": 270}]
    assert parse_antenna_direction("010-140 180-330") == [{"beam_start": 10, "beam_end": 140},
                                                          {"beam_start": 180, "beam_end": 330}]
    assert parse_antenna_direction("140 - 220, 260 - 100") == [{"beam_start": 140, "beam_end": 220},
                                                               {"beam_start": 260, "beam_end": 100}]
    assert parse_antenna_direction("190 - 40") == [{"beam_start": 190, "beam_end": 40}]
    assert parse_antenna_direction("45, 225") == [{"beam": 45}, {"beam": 225}]
    assert parse_antenna_direction("170, 190 - 220, 250 - 150") == [{"beam": 170},
                                                                    {"beam_start": 190, "beam_end": 220},
                                                                    {"beam_start": 250, "beam_end": 150}]
    assert parse_antenna_direction("0; 40 - 50; 90 - 140; 210 - 260; 290 – 300") == [{"beam": 0},
                                                                                      {"beam_start": 40, "beam_end": 50},
                                                                                      {"beam_start": 90, "beam_end": 140},
                                                                                      {"beam_start": 210, "beam_end": 260},
                                                                                      {"beam_start": 290, "beam_end": 300}]
    assert parse_antenna_direction("000 040-050 090-140 210-260 290–300") == [{"beam": 0},
                                                                              {"beam_start": 40, "beam_end": 50},
                                                                              {"beam_start": 90, "beam_end": 140},
                                                                              {"beam_start": 210, "beam_end": 260},
                                                                              {"beam_start": 290, "beam_end": 300}]


if __name__ == '__main__':
    pass
