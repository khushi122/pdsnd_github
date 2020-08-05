import time
import pandas as pd
#import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv'}
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June']
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def validate_city(city):
    """
    Checks user input for city.
    Returns:
        (str) city - name of the city to analyze
    """
    while city.lower() not in CITY_DATA:
        print('Oops! That is not a valid city name')
        city = input('Would you like to see data for Chicago, New York or Washington:\n')
    return city
def validate_month(month):
    """
    Checks user input for month.
    Returns:
        (str) month - name of the month to filter by
    """
    while month.title() not in MONTHS:
        print('Oops! That is not a valid month')
        month = input('Please enter for which month: January, February, March, April, May, June\n')
    return month
def validate_day(day):
    """
    Checks user input for day.
    Returns:
        (str) day - name of the day of week to filter by
    """
    while day.title() not in DAYS:
        print('Oops! That is not a valid day')
        day = input('Please enter for which day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday\n')
    return day
def validate_input(timeframe):
    """
    Checks userfor filtering the data by month, day, both or none.
    Returns:
        (str) month - name of the month to filter by
        (str) day - name of the day of week to filter by
        (str) both - name of the month and day of week to filter by
        (str) none - for unfiltered data
    """
    while timeframe.lower() not in ['month', 'day', 'both', 'none']:
        print('Oops! That is not a valid input')
        timeframe = input('Would you like to filter the data by month, day, both or not at all? Type "none" for no filter\n')
    return timeframe.lower()

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = input('Would you like to see data for Chicago, New York or Washington:\n')
    city = validate_city(city)

    month = ''
    day = ''

    timeframe = input('\nWould you like to filter the data by month, day, both or not at all? Type "none" for no filter\n')
    timeframe = validate_input(timeframe)
    if timeframe == 'month':
        month = validate_month(input('\nPlease enter for which month: January, February, March, April, May, June\n'))
        print('\nShowing {} data for {}'.format(city.title(), month.title()))
    elif timeframe == 'day':
        day = validate_day(input('\nPlease enter for which day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday\n'))
        day = validate_day(day)
        print('\nShowing {} data for {}'.format(city.title(), day.title()))
    elif timeframe == 'both':
        month = validate_month(input('\nPlease enter which month: January, February, March, April, May, June\n'))
        day = validate_day(input('\nPlease enter for which day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday\n'))
        print('\nShowing {} data for all {}s of {}\n'.format(city.title(), day.title(), month.title()))
    elif timeframe == 'none':
        print('\nShowing all data for {}'.format(city.title()))
    return city, month, day, timeframe

def load_data(city,month,day):
    """
    Loads data for the specified city and filters by month and/or day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month, day, both or neither
    """
    # load data into dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])
    # convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # convert End Time column to to_datetime
    df['End Time'] = pd.to_datetime(df['End Time'])
    # Create new column for month
    df['month'] = df['Start Time'].dt.month
    if month != '':
        # convert user input to equivalent month number
        month = MONTHS.index(month.title()) + 1
        # filter dataframe based on user input month
        df = df.loc[df['month'] == month]
    # create new day column
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # apply day filter to dataframe only if user has input day_name
    if day != '':
        # filter dataframe based on user input day_name
        df = df.loc[df['day_of_week'] == day.title()]
    return df

def loc_stats(var, col_name):
    start_time = time.time()
    location = var.value_counts().idxmax()
    if col_name == 'month':
        print('\nMost popular month: {}'.format(MONTHS[location - 1]))
        print('Number of trips: {}'.format(var.value_counts().max()))
        print('Execution time:', (time.time() - start_time))
    else:
        print('\nMost popular {}: {}'.format(col_name, location))
        print('Number of trips: {}'.format(var.value_counts().max()))
        print('Execution time:', (time.time() - start_time))

def time_stats(df, timeframe):
    """
    Calculates time statistics for the filtered or unfiltered data

    Args:
        (dataframe) df - pandas DataFrame containing city data filtered by month, day, both or neither
        (str) timeframe - parameter which is used to filter data (month, day, both, none)
    """
    print('\nCalculating time statistics')

    df['start_hour'] = df['Start Time'].dt.hour
    loc_stats(df['start_hour'], 'start hour')

    if timeframe == 'none' or timeframe == 'month':
        loc_stats(df['day_of_week'], 'day')
    if timeframe == 'none' or timeframe == 'day':
        loc_stats(df['month'], 'month')

    start_time = time.time()
    trip_duration = df['Trip Duration'].sum()
    avg_trip_duration = df['Trip Duration'].mean()
    print('\nTotal time of all trips: {}\nAverage time of all trips: {}'.format(trip_duration, avg_trip_duration))
    print('Number of trips made in total: {}'.format(df['Trip Duration'].shape[0]))
    print('Execution time:', (time.time() - start_time))

def station_stats(df):
    """
    Calculates location statistics for the filtered or unfiltered data

    Args:
        (dataframe) df - pandas DataFrame containing city data filtered by month, day, both or neither
    """
    print('\nCalculating location statistics')

    loc_stats(df['Start Station'], 'start station')
    loc_stats(df["End Station"], 'end station')
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']
    loc_stats(df['trip'], 'trip')

def user_stats(df,city):
    """
    Calculates user statistics for the filtered or unfiltered data

    Args:
        (dataframe) df - pandas DataFrame containing city data filtered by month, day, both or neither
        (str) city - city for which statistics are calculated
    """
    print('\nCalculating user statistics')

    start_time = time.time()
    user_types = df['User Type'].value_counts()
    print('\nNumber of different types of users:\n',user_types)
    print('Execution time:', (time.time() - start_time))

    if city.lower() != 'washington':

        start_time = time.time()
        gender = df['Gender'].value_counts()
        print('\nUsers of different genders:\n',gender)
        print('Execution time:', (time.time() - start_time))

        start_time = time.time()
        earliest_birth_year = df['Birth Year'].min()
        print('\nThe earliest year of birth is: {}'.format(earliest_birth_year))
        earliest_birth_year_users = df['Birth Year'].value_counts()[earliest_birth_year]
        print('Number of users with the earliest year of birth:', earliest_birth_year_users)
        print('Execution time:', (time.time() - start_time))

        start_time = time.time()
        latest_birth_year = df['Birth Year'].max()
        print('\nThe most recent year of birth is:', latest_birth_year)
        # number of users with the most recent year of Birth
        latest_birth_year_users = df['Birth Year'].value_counts()[latest_birth_year]
        print('Number of users with the most recent year of birth ({}):'.format(latest_birth_year),latest_birth_year_users)
        print('Execution time:', (time.time() - start_time))

        start_time = time.time()
        # find the most common year of birth
        loc_stats(df['Birth Year'], 'birth year')

def load_raw_data(city,counter):
    """
    Loads raw data as is 5 rows at a time

    Args:
        (int) counter - counter
        (str) city - city for which the raw data is displayed
    """
    df = pd.read_csv(CITY_DATA[city.lower()])
    if counter <= (df.shape[0])-1:
        print(df.loc[counter:counter+4])
    else:
        print('\nNo more data to show')
        exit()

def valid_input(raw_data):
    """
    Validates user input.
    Returns:
        (str) raw_data - yes: if user wants to see raw dat
                         no: if user does not want to see raw data
    """
    while raw_data not in ('yes', 'no'):
        print('\nOops! That is not a valid input')
        raw_data = input('Would you like to see raw data? Please enter "yes" or "no"\n')
    return raw_data

def main():
    while True:
        city, month, day, timeframe = get_filters()
        df = load_data(city, month, day)

        time_stats(df, timeframe)
        station_stats(df)
        user_stats(df, city)
        raw_data = valid_input(input('\nWould you like to see raw data? Type "yes" or "no"\n'))
        counter = 0
        while raw_data == 'yes':
            load_raw_data(city, counter)
            counter += 5
            raw_data = input('\nWould you like to see next 5 rows of raw data? yes or no\n')
            raw_data = valid_input(raw_data)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()