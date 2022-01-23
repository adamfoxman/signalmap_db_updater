import os
import base64
from math import ceil
from shutil import copyfile

from wand.image import Image
from wand.color import Color
import subprocess


# Find and replace a phrase in a file
def replace_in_file(file_path: str, find: str, replace: str):
    """
    Find and replace a phrase in a file

    :param file_path: Path to a file in a filesystem.
    :param find: Phrase to find in a file.
    :param replace: Phrase to replace in a file.
    :return: None
    """
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
    """
    Save a .scf file for a particular transmitter

    :param filepath: Path of a file in a filesystem.
    :param transmitter_type: Type of a transmitter (FM/DAB/TV)
    :return: Path to the .scf file.
    """
    try:
        if transmitter_type == 'f':
            copyfile('f.scf', f"{filepath}.scf")
        elif transmitter_type == 'd':
            copyfile('d.scf', f"{filepath}.scf")
        elif transmitter_type == 't':
            copyfile('t.scf', f"{filepath}.scf")
        else:
            raise Exception("Invalid transmitter type")
    except Exception as e:
        raise Exception("Could not copy .scf file")

    return filepath


def get_lrp_file(filepath: str) -> str:
    """
    Save a .lrp file for a particular transmitter

    :param filepath: Path of a file in a filesystem.
    :return: Path to the .lrp file.
    """
    try:
        copyfile('splat.lrp', f"{filepath}.lrp")
    except Exception as e:
        raise Exception("Could not copy .lrp file")

    return filepath


def file_exists(file_path: str) -> bool:
    """
    Check if a file exists

    :param file_path: Path to a file in a filesystem.
    :return: Boolean value indicating if the file exists.
    """
    return os.path.isfile(file_path)


def run_simulation(path: str,
                   location_filename: str,
                   transmitter_type: str,
                   erp: float,
                   frequency: float) -> str:
    """
    Run a simulation with the given parameters

    :param path: Path of a file in a filesystem.
    :param location_filename: Filename for the coverage files.
    :param transmitter_type: Type of a transmitter (FM/DAB/TV)
    :param erp: ERP power of a transmitter
    :param frequency: Frequency of a transmitter
    :return: Path to the simulation output file.
    """
    if transmitter_type == 't':
        receiver_height = 10
        db_threshold = 48
    elif transmitter_type == 'f':
        receiver_height = 10
        db_threshold = 48
    elif transmitter_type == 'd':
        receiver_height = 1.5
        db_threshold = 58
    else:
        receiver_height = 10
        db_threshold = 48

    # if ERP power is not given, use default value
    if erp == 0.0:
        erp = 1.0

    if erp < 0.1:
        coverage_radius = 150
    elif erp < 1:
        coverage_radius = 250
    elif erp < 5:
        coverage_radius = 350
    else:
        coverage_radius = 400

    location_filepath = f"{path}{location_filename}"

    erp_watts = ceil(erp * 1000)

    try:
        get_signal_color_file(location_filepath, transmitter_type)
        get_lrp_file(location_filepath)
    except Exception as e:
        print(e)

    if file_exists(f"{location_filepath}.qth") and file_exists(f"{location_filepath}.scf") and file_exists(f"{location_filepath}.az"):
        print("Files found")
    else:
        raise Exception("Files not found")

    splat_command = f'{os.getenv("SPLAT_PATH")}splat -t {location_filename} -erp {erp_watts} -f {frequency} -L {receiver_height} -R {coverage_radius} -gc 10.0 -db {db_threshold} -d {os.getenv("SRTM_PATH")} -metric -olditm -ngs -kml -N -o {location_filepath}.ppm'
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

    try:
        with Image(filename=f"{location_filepath}-ck.ppm") as img:
            with img.convert('png') as converted:
                converted.save(filename=f"{location_filepath}-ck.png")
    except Exception as e:
        print(e)
        return "error"

    replace_in_file(f"{location_filepath}.kml",
                    f"{location_filepath}.ppm",
                    f"https://storage.googleapis.com/signalmap-{transmitter_type}/{location_filename}.png")

    replace_in_file(f"{location_filepath}.kml",
                    f"{location_filepath}-ck.ppm",
                    f"https://storage.googleapis.com/signalmap-{transmitter_type}/{location_filename}-ck.png")

    return f"{location_filename}.png"


if __name__ == "__main__":
    pass

