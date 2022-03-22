from modules.style import Style


class Table:
    """
    A responsive table. Intended for displaying
    traffic data from vatsim.
    """

    def __init__(self):
        """
        Initally sets title, head and 
        rows to empty.
        """

        self.title = ""
        self.head = []
        self.rows = []

    def add_row(self, row):
        """
        Appends a row to the table.

        :param row: List of cells
        :type row: list
        """

        # Append passed row to rows list.
        self.rows.append(row)

    def __find_widest_cell(self):
        """
        Finds the widest cell in all
        cells and returns it.
        """

        # Create a list to hold the widest cells.
        lgst_cells = list()

        # Append widest head cell.
        lgst_cells.append(sorted(self.head, key=len)[-1])

        # Loop through rows.
        for row in self.rows:
            # Append widest row cell.
            lgst_cells.append(sorted(row, key=len)[-1])

        # Return the widest of the widest cells.
        return sorted(lgst_cells, key=len)[-1]   

    def __create_formatted_row(self, row):
        """
        Generates the code for a responsive 
        format string, executes it, and returns 
        the formatted string. The string is 
        formatted as a table row with a row width
        of the widest cell.
        """

        # Get the widest cell.
        global_cell_width = str(len(self.__find_widest_cell()))

        # Splitting code into parts at ".".
        # => string.format() where the string is part 1
        #    and format() is part 2.

        # Start of both parts
        string_part1 = "'"
        string_part2 = "format("

        # Piece together both parts.

        for i, cell in enumerate(row):
            # If last cell
            if i == (len(row) - 1):
                # Make string so it ends with a "|", 
                # Works as the end of a table row.
                string_part1 += "| {:<" + global_cell_width + "} |"

                # Feed the cell value to the format string
                string_part2 += f"'{cell}'"

            else:
                # Make string so it starts with a "|".
                # Works as the beginning of a table row,
                # and as a separater between cells.
                string_part1 += "| {:<" + global_cell_width + "} "

                # Feed the cell value to the format string
                string_part2 += f"'{cell}',"

        # End of both parts
        string_part1 += "'"
        string_part2 += ")"

        # Execute formatting and return formatted string
        return eval(f'{string_part1}.{string_part2}')

    def render(self):
        """
        Print finished table object to
        the command line.
        """

        # Get a formatted string of the head row.
        head_string = self.__create_formatted_row(row=self.head)

        # Start with empty divider line.
        line = ""

        # Index start at 0.
        i = 0

        # Generate a responsive divider line 
        # based on the head width.
        while i < len(head_string):
            line += "-"  # Add a dash.
            i += 1  # Increment index.
            
        # Create table head by combining divider lines 
        # with the formatted head string.
        head = f"{Style.txt_yellow(self.title)}\n{line}\n{head_string}\n{line}"
    
        # Start with empty body.
        body = ""

        # Loop through rows
        for i, row in enumerate(self.rows):
            # Add each formatted flight string to body
            body += "\n" + self.__create_formatted_row(row=row)

        # Create entire table by combining 
        # head, body and a divider line
        table = f"\n{head}{body}\n{line}\n"

        # Print table to command line
        print(table)
