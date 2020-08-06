import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv'}
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def validate_city(city):
    """Validate user input for city.

    Args:
        (str) city -> name of the city for which user wants to view data

    Return:
        (str) city - validated correct city name
    """

    while city.lower() not in CITY_DATA:
        print('Oops! That is not a valid city name')
        city = input('Would you like to see data for Chicago, New York or Washington:\n')
    return city

def validate_month(month):
    """Validate user input for month.

    Args:
        (str) month -> name of the month for which user wants to view data

    Return:
        (str) month - validated correct month name to filter the data by
    """

    while month.lower() not in MONTHS:
        print('Oops! That is not a valid month')
        month = input('Please enter for which month: January, February, March, April, May, June\n')
    return month

def validate_day(day):
    """Validate user input for day.

    Args:
        (str) day -> name of the day for which user wants to view data

    Return:
        (str) day - validated correct day of thhe week to filter the data by
    """

    while day.title() not in DAYS:
        print('Oops! That is not a valid day')
        day = input('Please enter for which day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday\n')
    return day

def validate_input(timeframe):
    """Validate user choice for filtering the data by month, day, both or none.

    Args:
        (str) timeframe -> user choice of timeframe to view data

    Return:
        (str) month - "month" if user chooses to filter by month
        (str) day - "day" if user chooses to filter by day of the week
        (str) both - "both" if user chooses to filter by both month and day of the week
        (str) none - "none" if user chooses to view unfiltered data
    """

    while timeframe.lower() not in ['month', 'day', 'both', 'none']:
        print('Oops! That is not a valid input')
        timeframe = input('Would you like to filter the data by month, day, both or not at all? Type "none" for no filter\n')
    return timeframe.lower()

def get_filters():
    """Take user input for a city, month, and/or day to filter data.

    Return:
        (str) city - name of the city to filter data
        (str) timeframe - user's choice of timeframe to filter data
        (str) month - name of the month to filter data
        (str) day - name of the day of week to filter data
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
    """Load data for the city of user's choice and for the timeframe specified by the user

    Args:
        (str) city - name of the city to filter data
        (str) month - name of the month to filter data
        (str) day - name of the day of week to filter data

    Return:
        df - pandas DataFrame containing city data filtered by month, day, both or neither
    """
    # load data into dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])
    # convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Create new column for month
    df['month'] = df['Start Time'].dt.month
    if month != '':
        # convert user input to equivalent month number
        month = MONTHS.index(month.lower()) + 1
        # filter dataframe based on user input month
        df = df.loc[df['month'] == month]
    # create new day column
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # apply day filter to dataframe only if user has input day_name
    if day != '':
        # filter dataframe based on user input day_name
        df = df.loc[df['day_of_week'] == day.title()]
    return df

def time_stats(df, timeframe):
    """Calculate time statistics for the filtered or unfiltered data

    Args:
        (dataframe) df - pandas DataFrame containing city data filtered by month, day, both or neither
        (str) timeframe - parameter which is used to filter data (month, day, both, none)

    Display descriptive results of the time statistics for the filtered data
    """
    print('\nCalculating time statistics')

    start_time = time.time()
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].value_counts().idxmax()
    print('\nMost popular Start hour: {}'.format(popular_hour))
    print('Number of trips started at most popular hour: {}'.format(df['hour'].value_counts().max()))
    print('Execution time:', (time.time() - start_time))

    start_time = time.time()
    if timeframe == 'none' or timeframe == 'day':
        popular_month = df['month'].value_counts().idxmax()
        popular_month = MONTHS[popular_month - 1].title()
        print('\nMost popular month: {}'.format(popular_month))
        print('Number of trips made during the most popular month: {}'.format(df['month'].value_counts().max()))
        print('Execution time:', (time.time() - start_time))

    start_time = time.time()
    if timeframe == 'none' or timeframe == 'month':
        popular_day = df['day_of_week'].value_counts().idxmax()
        print('\nMost popular day: {}'.format(popular_day))
        print('Number of trips made on the most popular day of the week: {}'.format(df['day_of_week'].value_counts().max()))
        print('Execution time:', (time.time() - start_time))

    start_time = time.time()
    trip_duration = df['Trip Duration'].sum()
    avg_trip_duration = df['Trip Duration'].mean()
    print('\nTotal time of all trips: {}\nAverage time of all trips: {}'.format(trip_duration, avg_trip_duration))
    print('Number of trips made in total: {}'.format(df['Trip Duration'].shape[0]))
    print('Execution time:', (time.time() - start_time))

def station_stats(df):
    """Calculate location statistics for the filtered or unfiltered data

    Args:
        (dataframe) df - pandas DataFrame containing city data filtered by month, day, both or neither

    Display descriptive results of the location statistics for the filtered data
    """
    print('\nCalculating location statistics')

    start_time = time.time()
    popular_start_station = df['Start Station'].value_counts().idxmax()
    print('\nMost commonly used start station is: {}'.format(popular_start_station))
    print('Number of trips started from the most popular start station: {}'.format(df['Start Station'].value_counts().max()))
    print('Execution time:', (time.time() - start_time))

    start_time = time.time()
    popular_end_station = df['End Station'].value_counts().idxmax()
    print('\nMost commonly used end station is: {}'.format(popular_end_station))
    print('Number of trips ended at the most popular end station: {}'.format(df['End Station'].value_counts().max()))
    print('Execution time:', (time.time() - start_time))

    start_time = time.time()
    df['trip'] = df['Start Station'] + ' and ' + df['End Station']
    popular_trip = df['trip'].value_counts().idxmax()
    print('\nMost trips are made between {}'.format(popular_trip))
    print('Number of the most popular trips: {}'.format(df['trip'].value_counts().max()))
    print('Execution time:', (time.time() - start_time))

def user_stats(df,city):
    """Calculate user statistics for the filtered or unfiltered data

    Args:
        (dataframe) df - pandas DataFrame containing city data filtered by month, day, both or neither
        (str) city - city for which statistics are calculated

    Display descriptive results of the user statistics for the filtered data
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
        # find the most recent year of birth
        latest_birth_year = df['Birth Year'].max()
        print('\nThe most recent year of birth is:', latest_birth_year)
        # number of users with the most recent year of Birth
        latest_birth_year_users = df['Birth Year'].value_counts()[latest_birth_year]
        print('Number of users with the most recent year of birth ({}):'.format(latest_birth_year),latest_birth_year_users)
        print('Execution time:', (time.time() - start_time))

        start_time = time.time()
        # find the most common year of birth
        most_common_birth_year = df['Birth Year'].value_counts().idxmax()
        print('\nThe most common year of birth:', most_common_birth_year)
        print('Number of users with the most common year of birth:', df['Birth Year'].value_counts().max())
        print('Execution time:', (time.time() - start_time))

def load_raw_data(city,counter):
    """Load raw data as is 5 rows at a time

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
    """Validate user input.

    Return:
        (str) raw_data - yes: if user wants to see raw data
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

        #Function call for time statistics of filtered data
        time_stats(df, timeframe)
        #Function call for location statistics of filtered data
        station_stats(df)
        #Function call for user statistics of filtered data
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
