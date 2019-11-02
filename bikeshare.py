import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for chicago, washington or new york city? ').lower()
        if city in ('chicago', 'washington', 'new york city'):
            break
        else:
            print('Please select either chicago, washington or new york city ')

    # get user input for month (all, january, february, ... , june)
    month_filter = input('Would you like to filter data by month? y / n ').lower()
    if month_filter == 'y':
        while True:
            month = input('Please select a month between january to june or select all: ').lower()
            if month in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
                break
            else:
                print('Please select a month between january to june or all ')
    else:
        month = 'all'

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_filter = input('Would you like to filter data by a day of week? y / n ').lower()
    if day_filter == 'y':
        while True:
            day = input('Please select a day of the week or all: ').title()
            if day in ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All'):
                break
            else:
                print('Please select a day of the week or all ')
    else:
        day = 'All'

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    #added a new column for route to help identify start-end pairs
    df['Route'] = df['Start Station'] + ' to ' + df['End Station']

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['hour'] = df['Start Time'].dt.hour
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    popular_month_index = df['month'].mode()[0]-1
    popular_month = months[popular_month_index]
    print('Most common month is: {}'.format(popular_month))

    # display the most common day of week
    popular_weekday = df['day_of_week'].mode()[0]
    print('Most common day of week is: {}'.format(popular_weekday))

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most common hour of day for trip start is: {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most common starting station is: {}'.format(popular_start_station))


    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most common ending station is: {}'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    popular_route = df['Route'].mode()[0]
    print('Most common route(start-end combination) is: {}'.format(popular_route))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_time_seconds = int(df['Trip Duration'].sum(axis = 0))
    counter = total_trip_time_seconds
    print('Total trip time across all trips is: {} seconds'.format(total_trip_time_seconds))
    #converted the total time travel to d:h:m:s format, for better legibility
    day = counter // (24 * 3600)
    counter = counter % (24 * 3600)
    hour = counter // 3600
    counter = counter % 3600
    minutes = counter // 60
    counter = counter % 60
    seconds = counter
    print('Total trip time across all trips in d:h:m:s is: {}:{}:{}:{} '.format(day, hour, minutes, seconds))

    # display mean travel time
    count_trips = df['Trip Duration'].count()
    average_trip_time_seconds = int(total_trip_time_seconds / count_trips)
    counter = average_trip_time_seconds
    print('Average trip duration is: {} seconds'.format(average_trip_time_seconds))
    avg_hour = counter // 3600
    counter = counter % 3600
    avg_minutes = counter // 60
    counter = counter % 60
    avg_seconds = counter
    print('Average trip duration in h:m:s is: {}:{}:{}'.format(avg_hour, avg_minutes, avg_seconds))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User type wise number of trips -')
    print(df['User Type'].value_counts())

    # Display counts of gender
    try:
        print('Genderwise number of trips -')
        print(df['Gender'].value_counts())
    except KeyError:
        print('Since genders are unavailable in washington data, we will skip that')

    # Display earliest, most recent, and most common year of birth
    try:
        oldest = df['Birth Year'].min()
        print('Oldest user was born in: {}'.format(oldest))
    except KeyError:
        print('Since birth years are unavailable in washington data, we will skip that')

    try:
        youngest = df['Birth Year'].max()
        print('Youngest user was born in: {}'.format(youngest))
    except KeyError:
        print('Since birth years are unavailable in washington data, we will skip that')

    try:
        popular_age = df['Birth Year'].mode()[0]
        print('Most common birth year is: {}'.format(popular_age))
    except KeyError:
        print('Since birth years are unavailable in washington data, we will skip that')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#print raw data for users
def print_data(df, size):
    i = 0
    #Confirm if they want to see any printed data
    print_raw_data = input('Would you like to see raw data? y / n ').lower()
    while print_raw_data == 'y':
        print(df[i:i+size])
        i += size
        print_raw_data = input('Would you like to see more raw data? y / n ').lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_data(df, 5)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
