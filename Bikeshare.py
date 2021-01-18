import time
import pandas as pd


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def input_validity(string):
    """ Checks for invalidity in the yes or no  response, takes in the string to display and returns the value"""
    while True:
        response = input(string).lower()
        if response in ['yes','no']:
            return response
        else:
            print('Invalid input!!!!! \n')

def filters_period(period, range_period):
    """
    Takes in two parameters a string and a list.
    Ask users to specify if they want to filter data based on the input(period)
    Make use of the range_period to ensure that the user doesn't put any invalid value
    Returns:
        string which shows which period would be use to filter the data or 'all' when no filter is required by the user
   """

    response =  input_validity('Would you like to filter the data by {}? Yes or No? \n'.format(period))
    if response == 'no':
        value = 'all'
    else:
    #handles invalid inputs by the user
        while True:

            value = input('Which {0}? {1}? \n' .format(period,', '.join(range_period))).title()
            if value in range_period:
                break
            else:
                print('Invalid input!!!!! \n')
    return value

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city_names = ['chicago', 'new york city', 'washington']
    month_names = ['January','February','March','April','May','June']
    day_names = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York City or Washington?\n ').lower()
        if city in city_names:
            break
        else:
            print('Invalid input!!!!! \n')


    # TO DO: get user input for month (all, january, february, ... , june)
    month = filters_period('month',month_names)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = filters_period('day',day_names)

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

    # convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] =  df['Start Time'].dt.month
    df['day_of_week'] =  df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':

      # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    list_month = ['January','February','March','April','May','June']
    most_common_month = list_month[df['month'].mode()[0]-1]
    # TO DO: display the most common month
    print('The most frequent month is', most_common_month)


    # TO DO: display the most common day of week
    print('\nThe most frequent day of the week is',df['day_of_week'].mode()[0])

    # TO DO: display the most common start hour
    print('\nThe most frequent start hour is', df['Start Time'].dt.hour.mode()[0])

    #Display the most common end hour
    print('\nThe most frequent end hour is', df['End Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('\nThe most popular start station is', df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print('\nThe most popular end station is', df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    print('\nThe most frequent combination of start and end station trip is', df.groupby(['Start Station','End Station']).size().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total travel time in second is ', df['Trip Duration'].sum())

    # TO DO: display mean travel time
    print('\nMean travel time in second is ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('The total counts of each user types are:\n', df['User Type'].value_counts())

    #if statement to avoid errors, by taking into consideration Washington which doesn't have the gender and birthyear columns
    if 'Gender' in df:
        # TO DO: Display counts of gender
        print('\nThe total counts per gender are:\n', df['Gender'].value_counts())

        # TO DO: Display earliest, most recent, and most common year of birth
        print('\n{0}, {1} and {2} are the earliest, most recent, and most common year of birth'.format(int(df['Birth Year'].min()),\
                                                                                                       int(df['Birth Year'].max()),\
                                                                                                       int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data_stats(df):
     """Displays five line of raw data upon request by user."""

     response = input_validity('Do you want to see 5 lines of raw data? Yes or No? ')

     if response == 'no':
        return
     else:
        print(df.head())
        c = 5
        while True:
           response = input_validity('Do you want to see more raw data? Yes or no? ')
           if response == 'no': break
           print(df.iloc[c:c+5])
           c+=5 #incrementing the counter to be able to read the next five elements
           if (c+5) > len(df): break  # breaks when the the counter is greater than the number of rows in the dataframe
     print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        time.sleep(4)
        station_stats(df)
        time.sleep(4)
        trip_duration_stats(df)
        time.sleep(4)
        user_stats(df)
        time.sleep(4)
        raw_data_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
