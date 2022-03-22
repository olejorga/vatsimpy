class Style:
    """
    Methods for styling a string.
    Intended to be used with print().
    """

    # Different style constants
    RESET = "\u001b[0m"  # Reset styling to defaults
    YELLOW = "\u001b[33;1m"  # Color yellow
    BLUE = "\u001b[34;1m"  # Color blue

    @classmethod
    def txt_yellow(cls, string):
        """
        Make passed string red and 
        return it.

        :param string: String to be colored:
        :type string: str

        :return string: Colored string
        :rtype: str
        """

        # Color string, reset styling and return string
        return cls.YELLOW + string + cls.RESET

    @classmethod
    def txt_blue(cls, string):
        """
        Make passed string blue and
        return it.

        :param string: String to be colored:
        :type string: str

        :return string: Colored string
        :rtype: str
        """

        # Color string, reset styling and return string
        return cls.BLUE + string + cls.RESET
