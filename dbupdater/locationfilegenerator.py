def get_location_file(path: str,
                      external_id: int,
                      transmitter_type: str,
                      country: str,
                      station_name: str,
                      latitude: float,
                      longitude: float,
                      elevation: int,
                      ) -> str:
    """
    Generates a location file for the database.

    Parameters
    ----------
    path : str
        The path to the location file.
    external_id : int
        The external id of a transmitter.
    transmitter_type : str
        The type of the transmitter.
    country : str
        The country of the location.
    station_name : str
        The name of the station.
    latitude : float
        The latitude of the location.
    longitude : float
        The longitude of the location.
    elevation : int
        The elevation of the location.

    Returns
    -------
    str
        The location filename .
    """
    if path[-1] != '/':
        path += '/'
    location_filename = f"{country}_{transmitter_type}_{external_id}.qth"
    location_path = f"{path}{location_filename}"
    try:
        with open(location_path, 'w+') as location_file:
            location_file.write(f"{station_name}\n")
            location_file.write(f"{latitude}\n")
            location_file.write(f"{longitude * -1}\n")
            location_file.write(f"{elevation} meters")
    except FileNotFoundError:
        print(f"Error: {location_filename} not found.")

    return location_filename


