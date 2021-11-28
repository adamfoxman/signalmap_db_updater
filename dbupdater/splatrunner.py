import os
from math import ceil

from wand.image import Image
from wand.color import Color
import subprocess

def run_simulation(path: str,
                   external_id: int,
                   transmitter_type: str,
                   country: str,
                   erp: float) -> str:
    if transmitter_type == 't':
        receiver_height = 10
        db_threshold = 48
    elif transmitter_type == 'f':
        receiver_height = 10
        db_threshold = 34
    elif transmitter_type == 'd':
        receiver_height = 1.5
        db_threshold = 58
    else:
        receiver_height = 10
        db_threshold = 48

    location_filename = f"{country}_{transmitter_type}_{external_id}"
    location_filepath = f"{path}{location_filename}"

    erp_watts = ceil(erp * 1000)

    splat_command = f'{os.getenv("SPLAT_PATH")}splat -t {location_filename} -erp {erp_watts} -L {receiver_height} -R 50 -gc 10.0 -db 34 -d {os.getenv("SRTM_PATH")} -metric -olditm -ngs -kml -N -o {location_filepath}.ppm'
    try:
        subprocess.run(splat_command, shell=True)
    except subprocess.CalledProcessError as e:
        print(e)
        return "error"

    try:
        with Image(filename=f"{location_filepath}.ppm") as img:
            img.transparent_color(color=Color('#fff'), alpha=0.0)
            img.transparentize(0.25)
            with img.convert('png') as converted:
                converted.save(filename=f"{location_filepath}.png")
    except Exception as e:
        print(e)
        return "error"

    replace_in_file(f"{location_filepath}.kml", f"{location_filepath}.ppm", f"{location_filepath}.png")

    return f"{location_filename}.png"


# Find and replace a phrase in a file
def replace_in_file(file_path: str, find: str, replace: str):
    try:
        with open(file_path, 'r') as file:
            filedata = file.read()
        filedata = filedata.replace(find, replace)
        with open(file_path, 'w') as file:
            file.write(filedata)
    except Exception as e:
        print(e)


def get_signal_color_file(filepath: str, transmitter_type: str) -> str:
    if transmitter_type == 'f':
        pass
    elif transmitter_type == 'd':
        pass
    elif transmitter_type == 't':
        pass
    else:
        return "invalid"
