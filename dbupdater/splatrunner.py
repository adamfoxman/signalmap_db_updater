import os
import base64
from math import ceil

from wand.image import Image
from wand.color import Color
import subprocess


def run_simulation(path: str,
                   location_filename: str,
                   transmitter_type: str,
                   erp: float) -> str:
    """
    Run a simulation with the given parameters

    :param path: Path of a file in a filesystem.
    :param location_filename: Filename for the coverage files.
    :param transmitter_type: Type of a transmitter (FM/DAB/TV)
    :param erp: ERP power of a transmitter
    :return:
    """
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

    location_filepath = f"{path}{location_filename}"

    erp_watts = ceil(erp * 1000)

    try:
        get_signal_color_file(location_filepath, transmitter_type)
    except Exception as e:
        print(e)

    if file_exists(f"{location_filepath}.qth") and file_exists(f"{location_filepath}.scf") and file_exists(f"{location_filepath}.az"):
        print("Files found")
    else:
        raise Exception("Files not found")

    splat_command = f'{os.getenv("SPLAT_PATH")}splat -t {location_filename} -erp {erp_watts} -L {receiver_height} -R 100 -gc 10.0 -db {db_threshold} -d {os.getenv("SRTM_PATH")} -metric -olditm -ngs -kml -N -o {location_filepath}.ppm'
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


# save .scf file for a particular transmitter
def get_signal_color_file(filepath: str, transmitter_type: str) -> str:
    if transmitter_type == 'f':
        file_r = open("f.scf", 'r')
    elif transmitter_type == 'd':
        file_r = open("d.scf", 'r')
    elif transmitter_type == 't':
        file_r = open("t.scf", 'r')
    else:
        raise Exception("Invalid transmitter type")

    try:
        filedata = file_r.read()
        with open(f"{filepath}.scf", 'w') as file_w:
            file_w.write(filedata)
            file_w.close()
        file_r.close()
    except Exception as e:
        print(e)
        raise Exception("Could not write signal color file")

    return filepath


# encode file as base64 string
def encode_file(file_path: str) -> str:
    with open(file_path, 'rb') as file:
        return base64.b64encode(file.read()).decode('utf-8')


# load kml file as string
def load_kml_file(file_path: str) -> str:
    if not os.path.isfile(file_path):
        raise Exception("File not found")
    if not file_path.endswith(".kml"):
        raise Exception("File is not a kml file")
    else:
        with open(file_path, 'r') as file:
            return file.read()


# check if file exists
def file_exists(file_path: str) -> bool:
    return os.path.isfile(file_path)