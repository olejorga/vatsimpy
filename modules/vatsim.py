import urllib.request
import urllib.error
import json
import logging
import os
from datetime import datetime


class Vatsim:
    """
    A datahandler for getting vatsim data.

    :param local_mode: Run datahandler with local test data
    :type local_mode: bool

    :param debug_mode: Log debug messages
    :type debug_mode: bool
    """

    def __init__(self, local_mode=False, debug_mode=False):
        """
        Initially, cached data is looked for, retrived and 
        checked if outdated. If true, new data or test data 
        is fetched, depending on the boolean state of local_mode.

        :param local_mode: Run datahandler with local test data
        :type local_mode: bool

        :param debug_mode: Log debug messages
        :type debug_mode: bool
        """
        
        # URLs and paths to the vatsim data
        self.live_data_url = "https://data.vatsim.net/v3/vatsim-data.json"
        self.test_data_path = "data/vatsim-data.json"
        self.cached_data_path = "cache/vatsim.json"

        # Save local mode boolean for later referance
        self.local_mode = local_mode

        # Adds x number of min to the data update interval.
        # Because the new vatsim data is sometimes late,
        # despite what the update interval is.
        # This fix tries to prevent fetching old data.
        self.update_delay = .5

        # If debug mode is passed as true, turn on debug in logging. 
        # (activates all levels of logging debug->critical)
        # (default warning->critical)
        if debug_mode:
            logging.getLogger().setLevel(logging.DEBUG)

        # This is the main variable for vatsim data.
        # This dict will be manipulated by the various core methods.
        self.vatsim_data = {}

        # Check if cached data exists on instance creation.
        self.__is_data_cached()

        # Check if data is outdated on instance creation.
        self.__is_data_outdated()

    """
    __CORE METHODs

    Intended for use internally in class.
    Methods for processing the vatsim data.
    """

    def __is_data_cached(self):
        """
        Checks if the cached data file exists. If true,
        cached data is retrived. If not, local test data
        or new data is fetched, depending on the boolean
        state of local_mode.
        """

        # Check if cache file exists
        if os.path.exists(self.cached_data_path):
            # A debug message for easier development.
            logging.debug('Data is cached')
            logging.debug('Fetching cached data')

            # Fetch local cached data
            self.__fetch_local_data(path=self.cached_data_path)

        # If local_mode is true, fetch local test data instead.
        elif self.local_mode:
            # A debug message for easier development.
            logging.debug('Data is not cached')
            logging.debug('Fetching local test data')

            # Fetch local test data
            self.__fetch_local_data(path=self.test_data_path)

        else:
            # A debug message for easier development.
            logging.debug('Data is not cached')
            logging.debug('Fetching new live data')
            
            # Fetch new live data
            self.__fetch_new_data()

    def __is_data_outdated(self):
        """
        Checks if data is outdated. If true, 
        local test data or new data is fetched,
        depending on the boolean state of local_mode. 
        """

        # Get the timestring of the current data was updated (utc time).
        last_update_timestring = self.vatsim_data['general']['update']

        # Get the current update interval.
        update_interval = self.vatsim_data['general']['reload'] + self.update_delay

        # Get current datetime in (utc time).
        time_now = datetime.utcnow()

        # Convert timestring to a datetime (Format: YYYYMMDDhhmmss).
        time_then = datetime.strptime(last_update_timestring, "%Y%m%d%H%M%S")

        # Calculate diff between now and the last update
        # in minutes.
        time_diff = time_now - time_then
        time_diff = time_diff.total_seconds() / 60
        
        # If differance is greater then the update interval,
        # fetch new live data.
        if time_diff > update_interval and not self.local_mode:
            # A debug message for easier development.
            logging.debug('Data is outdated')
            logging.debug('Fetching new live data')

            # Fetch new live data
            self.__fetch_new_data()
        
        # If local mode is true as well, fetch local test data.
        elif time_diff > update_interval and self.local_mode:
            # A debug message for easier development.
            logging.debug('Data is outdated')
            logging.debug('Fetching local test data')

            # Fetch local test data
            self.__fetch_local_data(path=self.test_data_path)

        else:
            # A debug message for easier development.
            logging.debug('Data is up to date')

    def __fetch_local_data(self, path):
        """
        Fetches a local data file from 
        passed path and caches it.

        Data is also stored in the 
        vatsim_data variable.

        :param path: Local path to file
        :type path: str
        """

        try:
            # Load and parse local data file
            with open(path) as file:
                parsed_json = json.load(file)

        except FileNotFoundError as e:
            # Log error with tip
            logging.error(f'{e}\n- Please check path')

        except json.JSONDecodeError as e:
            # Log error with tip
            logging.error(f'{e}\n- Data is not valid json')

        else:
            # A debug message for easier development.
            logging.debug('Copying data to self.vatsim_data')

            # Save parsed data in vatsim_data
            self.vatsim_data = parsed_json

            # A debug message for easier development.
            logging.debug('Caching data')

            # Cache gotten data
            self.__cache_data()

    def __fetch_new_data(self):
        """
        Fetches live vatsim data from
        live_data_url and caches it. 

        Data is also stored in the 
        vatsim_data variable.
        """

        try:
            # Request and parse live data file
            with urllib.request.urlopen(self.live_data_url) as res:
                parsed_json = json.load(res)

        except urllib.error.HTTPError as e:
            # Log error with tip
            logging.error(f'{e}\n- Please check url')

            # Run fail safe
            self.__fail_safe()

        except urllib.error.URLError as e:
            # Log error with tip
            logging.error(f'{e}\n- Please check internet connection')

            # Run fail safe
            self.__fail_safe()

        else:
            # A debug message for easier development.
            logging.debug('Copying data to self.vatsim_data')

            # Save parsed data in vatsim_data
            self.vatsim_data = parsed_json

            # A debug message for easier development.
            logging.debug('Caching data')

            # Cache gotten data
            self.__cache_data()

    def __cache_data(self):
        """
        Stores the vatsim data to the
        cache file at cached_data_path.
        """

        try:
            # Write vatsim data to cache file
            with open(self.cached_data_path, 'w') as file:
                json.dump(self.vatsim_data, file)

        except FileNotFoundError as e:
            # Log error with tip
            logging.error(f'{e}\n- Please check path')

        except json.JSONDecodeError as e:
            # Log error with tip
            logging.error(f'{e}\n- Data is not valid json')

    """
    GET METHODs

    Intended for use on instance of class & internally
    Methods for getting specific bits of the vatsim data
    """

    def get_flights(self):
        """
        Gets a list of all flights and 
        returns them.

        :return: List of flights. Empty list if no flights were found
        :rtype: list
        """

        # Check if vatsim data is outdated
        # (always do this, incase method is called by itself)
        self.__is_data_outdated()

        # Return all the pilots on the network
        return self.vatsim_data['pilots']

    def get_flights_by_dep(self, icao):
        """
        Gets a list of flights based on its 
        departure airport icao code.

        :param icao: Dest airport icao
        :type icao: str

        :return: A list of flights. Empty list if no flights were found
        :rtype: list
        """

        # Check if vatsim data is outdated
        # (always do this, incase method is called by itself)
        self.__is_data_outdated()

        # Get all flights on the network
        flights = self.get_flights()

        # Find all flights departing the specified airport
        departures = []

        for flight in flights:
            if flight['flight_plan']:
                if flight['flight_plan']['departure'] == icao:
                    departures.append(flight)

        # Return departing flights
        return departures

    def get_flights_by_dest(self, icao):
        """
        Gets a list of flights based on its 
        destination airport icao code.

        :param icao: Dest airport icao
        :type icao: str

        :return: A list of flights. Empty list if no flights were found
        :rtype: list
        """

        # Check if vatsim data is outdated
        # (always do this, incase method is called by itself)
        self.__is_data_outdated()

        # Get all flights on the network
        flights = self.get_flights()

        # Find all flights arriving at the specified airport
        arrivals = []

        for flight in flights:
            if flight['flight_plan']:
                if flight['flight_plan']['arrival'] == icao:
                    arrivals.append(flight)

        # Return arriving flights
        return arrivals

    """
    EXTRA METHODs

    ...
    """

    def __fail_safe(self):
        """
        An extra method for switching to local_mode if
        a http or connection error is raised when fetching
        new live data. This ensures that the program is
        able to display some data when "you" are assessing
        this project.
        """

        # Display a warning message, letting the user know
        # the program is swtiching to local mode.
        logging.warning('Switching to local mode')

        # Set local_mode to true.
        self.local_mode = True

        # A debug message for easier development.
        logging.debug('Fetching local test data')

        # Fetch local test data
        self.__fetch_local_data(path=self.test_data_path)
