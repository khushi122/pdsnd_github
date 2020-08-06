import constants as ct

class Validation:

    def validate_city(self, city):
        """
        Checks user input for city.
        Returns:
        (str) city - name of the city to analyze
        """
        while city.lower() not in ct.CITY_DATA:
            print('Oops! That is not a valid city name')
            city = input('Would you like to see data for Chicago, New York or Washington:\n')
        return city

    def validate_timeframe(self, timeframe):
        """
        Checks userfor filtering the data by month, day, both or none.
        Returns:
            (str) month - name of the month to filter by
            (str) day - name of the day of week to filter by
            (str) both - name of the month and day of week to filter by
            (str) none - for unfiltered data
        """
        while timeframe.lower() not in ('month', 'day', 'both', 'none'):
            print('Oops! That is not a valid input')
            timeframe = input('Would you like to filter the data by month, day, both or not at all? Type "none" for no filter\n')
        return timeframe.lower()

    def validate_month(self, month):
        """
        Checks user input for month.
        Returns:
        (str) month - name of the month to filter by
        """
        while month.title() not in ct.MONTHS:
            print('Oops! That is not a valid month')
            month = input('Please enter for which month: January, February, March, April, May, June\n')
        return month

    def validate_day(self, day):
        """
        Checks user input for day.
        Returns:
        (str) day - name of the day of week to filter by
        """
        while day.title() not in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'):
            print('Oops! That is not a valid day')
            day = input('Please enter for which day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday\n')
        return day

    def validate_input(self, choice):
        """
        Validates user input.
        Returns:
            (str) choice - yes: if user wants to see raw data or if user wants to restart the program
                           no: if user does not want to see raw data or if user wants to exit the program
        """
        while choice.lower() not in ('yes', 'no'):
            print('\nOops! That is not a valid input')
            choice = input('Would you like to see raw data? Please enter "yes" or "no"\n')
        return choice
