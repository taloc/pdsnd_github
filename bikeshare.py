import time
import pandas as pd


cities = {'chicago': 'chicago.csv',
          'new york': 'new_york_city.csv',
          'washington': 'washington.csv'}


months = {'january': '01',
          'february': '02',
          'march': '03', 'april': '04',
          'may': '05',
          'june': '06', 'all': ('01', '02', '03', '04', '05', '06')}

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

# User needs to filter data to specify a city, month and day of the week. Option for multiple selection using all
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

    #Loop to get city input from user
    while True:
        city = input('Enter city name: \n').lower()
        if city in cities.keys():
            print('Thank you, you have selected {},'.format(city.title()),
                  'now specify the month to be analyzed.')
            break
        else:
            print('You entered {},'.format(city.title()),
                  'unfortunately we don\'t have data from that city, please choose from Chicago, Washington or New York')
            continue

    # Loop to get user input for month (all, january, february, ... , june)
    while True:
        month = input('Enter month from only these options January, February, March, April, May, June, or all: \n').lower()
        if month in months.keys():
            print('Thank you, you have selected {},'.format(month.title()),
                  'now please select the day to be analyzed.')
            break
        else:
            print('You entered {},'.format(month.title()),
                  'unfortunately we don\'t have data for that, please choose from January, February, March, April, May or June, or all\n')
            continue

    # Loop to get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input(
            'Select among Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all: \n').lower())
        if day in days:
            print('Ok, an analysis will be created for {};'.format(city.title()), 'Month to be analyzed: {};'.format(month.title()), 'Day to be analyzed: {}'.format(day.title()))
            break
        else:
            print('You entered {},'.format(day.title()), 'unfortunately that\'s not and option, please try again.\n')
            continue

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
    #Use of pandas to read the csv files, and creation of columns
    df = pd.read_csv(cities[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    df['day_name'] = df['Start Time'].dt.weekday_name
    if day != 'all':
        df = df[df['day_name'] == day.title()]

    df['hour'] = df['Start Time'].dt.hour
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    # Mode for month
    common_month = df['month'].mode()[0]
    if common_month == 1:
        common_month = "January"
    elif common_month == 2:
        common_month = "February"
    elif common_month == 3:
        common_month = "March"
    elif common_month == 4:
        common_month = "April"
    elif common_month == 5:
        common_month = "May"
    else:
        common_month = "June"
    print('The most common month:', common_month)


    # Mode for day
    common_day_name = df['day_name'].mode()[0]
    print('The most common day of the week:', common_day_name)

    # Mode for start hour
    common_hour = df['Start Time'].dt.hour.mode()[0]
    print('The most common hour (24 hrs):', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Will display the most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('Most used start station:', common_start)

    #Will display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('Most used end station:', common_end)

    #Will display most frequent combination of start station and end station trip
    common_trip = (df['Start Station'] + ' and ' + df['End Station']).mode()[0]
    print('The most common trip is between: ', common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Will display total travel time
    total_travel = df['Trip Duration'].sum()

    #Will display mean travel time
    avg_travel = df['Trip Duration'].mean()
    print("Total travel time: ", total_travel)
    print("Average travel time: ", avg_travel)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    #A try and except method is used for the missing columns in the Washington csv file
    try:
        # Display counts of user types
        user_types = df['User Type'].value_counts()
        # Display counts of gender
        count_gender = df['Gender'].value_counts()
        # Display earliest, most recent, and most common year of birth
        earliest_birthdate = df['Birth Year'].min()
        most_recent_birthdate = df['Birth Year'].max()
        most_common_birthdate = df['Birth Year'].mode()

        print(user_types)

        print(count_gender)
        print("Earliest birthdate: ", int(earliest_birthdate))

        print("Most recent birthdate: ", int(most_recent_birthdate))

        print("Most common birthdate: ", int(most_common_birthdate))
    except KeyError:
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    '''Asks for 5 rows of data '''

    #Option for user to display raw data
    raw_data_request = input('\nDo you want to see 5 rows of raw data?  Yes or No\n> ').lower()
    if raw_data_request == 'yes':
        start_time = time.time()
        i = 0
        while True:
            print(df.iloc[i:i + 5])
            i += 5
            print("\nThis took %s seconds." % (time.time() - start_time))
            more_data_request = input('\nWould you like to see 5 more rows of raw data?  Yes or No\n> ').lower()

            if more_data_request != 'yes':
                break

    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        restart = input('\nTo restart select: yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
