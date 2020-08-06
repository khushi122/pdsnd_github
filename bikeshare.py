import time
import sys
import pandas as pd
import validation as vd
import constants as ct

# Create instance of class Validation
validation = vd.Validation()
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    month = ''
    day = ''

    city = validation.validate_city(input('Would you like to see data for Chicago, New York or Washington:\n'))
    timeframe = validation.validate_timeframe(input('\nWould you like to filter the data by month, day, both or not at all? Type "none" for no filter\n'))
    if timeframe == 'month':
        month = validation.validate_month(input('\nPlease enter for which month: January, February, March, April, May, June\n'))
        print('\nShowing {} data for {}'.format(city.title(), month.title()))
    elif timeframe == 'day':
        day = validation.validate_day(input('\nPlease enter for which day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday\n'))
        print('\nShowing {} data for {}'.format(city.title(), day.title()))
    elif timeframe == 'both':
        month = validation.validate_month(input('\nPlease enter which month: January, February, March, April, May, June\n'))
        day = validation.validate_day(input('\nPlease enter for which day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday\n'))
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
    df = pd.read_csv(ct.CITY_DATA[city.lower()])
    # convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # convert End Time column to to_datetime
    df['End Time'] = pd.to_datetime(df['End Time'])
    # Create new column for month
    df['month'] = df['Start Time'].dt.month
    # apply month filter to dataframe only if user has input month name
    if month != '':
        # convert user input to equivalent month number
        month = ct.MONTHS.index(month.title()) + 1
        # filter dataframe based on month number
        df = df.loc[df['month'] == month]
    # create new column for day of the week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # apply day filter to dataframe only if user has input day_name
    if day != '':
        # filter dataframe based on user input day_name
        df = df.loc[df['day_of_week'] == day.title()]
    return df

def loc_stats(var, col_name):
    """
    calculate statistical data

    Args:
        (str) var - dataframe column to be used for calculation
        (str) col_name - string to be used to display descriptive messages
    """
    start_time = time.time()
    stats_var = var.value_counts().idxmax()
    if col_name == 'month':
        print('\nMost popular month: {}'.format(ct.MONTHS[stats_var - 1].title()))
        print('Number of trips: {}'.format(var.value_counts().max()))
        print('Execution time:', (time.time() - start_time))
    else:
        print('\nMost popular {}: {}'.format(col_name, stats_var))
        print('Number of trips: {}'.format(var.value_counts().max()))
        print('Execution time:', (time.time() - start_time))

def time_stats(df, timeframe):
    """
    Calculate time statistics for the filtered or unfiltered data

    Args:
        (dataframe) df - pandas DataFrame containing city data filtered by month, day, both or neither
        (str) timeframe - parameter which is used to filter data (month, day, both, none)
    """
    print('\nCalculating time statistics')
    #create new column for hour by extracting from start time column
    df['start_hour'] = df['Start Time'].dt.hour
    loc_stats(df['start_hour'], 'start hour')
    #create new column for hour by extracting from end time column
    df['end_hour'] = df['End Time'].dt.hour
    loc_stats(df['end_hour'], 'end hour')

    if timeframe == 'none' or timeframe == 'month':
        loc_stats(df['day_of_week'], 'day')
    elif timeframe == 'none' or timeframe == 'day':
        loc_stats(df['month'], 'month')

    start_time = time.time()
    print('\nTotal time for all trips: {}\nAverage time for all trips: {}'.format(df['Trip Duration'].sum(), df['Trip Duration'].mean()))
    print('Total number of trips made: {}'.format(df['Trip Duration'].shape[0]))
    print('Execution time:', (time.time() - start_time))

def station_stats(df):
    """
    Calculate location statistics for the filtered or unfiltered data

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
    Calculate user statistics for the filtered or unfiltered data

    Args:
        (dataframe) df - pandas DataFrame containing city data filtered by month, day, both or neither
        (str) city - city for which statistics are calculated
    """
    print('\nCalculating user statistics')

    start_time = time.time()
    print('\nNumber of different types of users:\n', df['User Type'].value_counts())
    print('Execution time:', (time.time() - start_time))

    if city.lower() != 'washington':

        start_time = time.time()
        print('\nUsers of different genders:\n',df['Gender'].value_counts())
        print('Execution time:', (time.time() - start_time))

        start_time = time.time()
        print('\nThe earliest year of birth: {}'.format(df['Birth Year'].min()))
        print('Number of users with the earliest year of birth:', df['Birth Year'].value_counts()[df['Birth Year'].min()])
        print('Execution time:', (time.time() - start_time))

        start_time = time.time()
        print('\nThe most recent year of birth:', df['Birth Year'].max())
        print('Number of users with the most recent year of birth:', df['Birth Year'].value_counts()[df['Birth Year'].max()])
        print('Execution time:', (time.time() - start_time))

        loc_stats(df['Birth Year'], 'birth year')

def load_raw_data(city,counter):
    """
    Load raw data as is 5 rows at a time

    Args:
        (int) counter - counter
        (str) city - city for which the raw data is displayed
    """
    df = pd.read_csv(ct.CITY_DATA[city.lower()])
    if counter <= (df.shape[0])-1:
        print(df.loc[counter:counter+4])
    else:
        print('\nNo more data to show')

def main():
    while True:
        city, month, day, timeframe = get_filters()
        df = load_data(city, month, day)
        time_stats(df, timeframe)
        station_stats(df)
        user_stats(df, city)
        choice_rawData = validation.validate_input(input('\nWould you like to see raw data? Type "yes" or "no"\n'))
        counter = 0
        while choice_rawData.lower() == 'yes':
            load_raw_data(city, counter)
            counter += 5
            choice_rawData = validation.validate_input(input('\nWould you like to see next 5 rows of raw data? yes or no\n'))

        choice = validation.validate_input(input('\nWould you like to restart? Enter yes or no.\n'))
        if choice.lower() == 'no':
            sys.exit()

if __name__ == "__main__":
	main()
