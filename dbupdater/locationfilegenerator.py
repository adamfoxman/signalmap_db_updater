import logging

def get_location_file(path: str,
                      location_filename: str,
                      station_name: str,
                      latitude: float,
                      longitude: float,
                      elevation: int,
                      ) -> str:
    """
    Generates a location file for the given parameters.

    :param path: Path for a file in a filesystem.
    :param external_id: External ID of the transmitter.
    :param transmitter_type: Type of the transmitter (FM/DAB/TV).
    :param country: ISO country code.
    :param station_name: Transmitted station name.
    :param latitude: Latitude location of the transmitter.
    :param longitude: Longitude location of the transmitter.
    :param elevation: Elevation of an antenna above the ground.
    :return: Filename for a generated file.
    """
    if path[-1] != '/':
        path += '/'
    location_path = f"{path}{location_filename}.qth"

    if elevation is None:
        # Assume 100 meters if no elevation is given.
        elevation = 100
    try:
        with open(location_path, 'w+') as location_file:
            location_file.write(f"{station_name}\n")
            location_file.write(f"{latitude}\n")
            location_file.write(f"{longitude * -1}\n")
            location_file.write(f"{elevation} meters")
    except FileNotFoundError:
        logging.error(f"Could not write location file to {location_path}.")
        print(f"Error: {location_filename} not found.")

    return location_filename


if __name__ == "__main__":
    pass
