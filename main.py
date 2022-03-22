from modules.vatsim import Vatsim
from modules.style import Style
from modules.table import Table


def main():
    """
    Main program flow:
    1. Initialize vatism data.
    2. Run dialog.
    3. Repeat forever.
    """

    # Print intro.
    print(Style.txt_blue(
        r'---------------------------''\n'
        r'| Welcome to...           |''\n'
        r'|   \/ATSIM TRAFFIC TABLE |''\n'
        r'---------------------------''\n''\n'
        r'Initalizing vatsim data...''\n'
    ))

    # 1: Initalize vatsim data.
    vsim = Vatsim()

    # Let user know, initalization is complete.
    print(Style.txt_blue('Vatsim data Initalized.\n'))

    def dialog():
        """
        Prompts user to enter desired airport 
        icao code and get corresponding 
        traffic data.
        """

        # Get the user's desired icao.
        user_icao = input('Enter airport icao (e.g. EGLL) ')

        # If the user's inputted icao is alphanumeric and 
        # exactly 4 charachters long, continue program.
        if user_icao.isalnum() and len(user_icao) == 4:
            # Force icao to upper case. 
            # (this is the standard in the vatsim dataset)
            user_icao = user_icao.upper()

            # Let user know this is traffic at their desired airport
            print(Style.txt_blue(f'Loading traffic at {user_icao}...'))

            # Get the departures at the desired airport.
            dep_flights = vsim.get_flights_by_dep(icao=user_icao)

            # Get the departures at the desired airport.
            arr_flights = vsim.get_flights_by_dest(icao=user_icao)

            # Create tables
            dep_table = Table()
            arr_table = Table()

            # Set title for table
            dep_table.title = f"{user_icao} DEPARTURES"
            arr_table.title = f"{user_icao} ARRIVALS"

            # Set head cells for both tables
            dep_table.head = ['Flight', 'To']
            arr_table.head = ['Flight', 'From']

            # Create a row for each flight in each table
            for dep in dep_flights:
                dep_table.add_row(
                    [dep['callsign'], dep['planned_destairport']]
                )         
            for arr in arr_flights:
                arr_table.add_row(
                    [arr['callsign'], arr['planned_depairport']]
                )

            # Render tables to cli
            dep_table.render()
            arr_table.render()

            # Calculate total number of flights
            total_flights = len(dep_flights) + len(arr_flights)

            # Let user know how many flights there are
            print(f'{total_flights} flights ({len(dep_flights)} departures and {len(arr_flights)} arrivals)\n')

        else: 
            # Let user know what they did wrong
            print(Style.txt_yellow('Icao must be alphanumeric and 4 characters long.'))

            # Re-run dialog
            dialog()

    # 3: Repeat forever.
    while True:
        # 2: Run dialog.
        dialog()


# Run program if main is run by itself.
# (not in a import)
if __name__ == "__main__":
    main()
