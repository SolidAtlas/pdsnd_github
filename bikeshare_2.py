import time
import pandas as pd


###############-------files to call-------######################
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


###############-------global variables-------###################
cities = ['chicago','new york city','washington']
months = ['january','february','march','april','may','june']
weekday = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

months_options = ['all','january','february','march','april','may','june']
weekday_options = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']

answers = ['yes', 'no']
answer = 'yes'

iterator = 0

###############-------Functions-------##########################

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('The options for cities are:')
    print('Chicago, New York City, Washington')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input('Choose a city for analysis:   ')).lower()
            if city in cities:
                print('GOOD CHOICE!')
                break
            else:
                 print('\nBad User...choose an AVAILABLE option\nOptions:\nChicago, New York City, Washington')
        except:
            print('That is not a valid selection, Please choose again')
            print('Options:')
            print('Chicago, New York City, Washington')

    # get user input for month (all, january, february, ... , june)
    print('The options for months are:')
    print('January, February, March, April, May, June')
    while True:
        try:
            month = str(input('Choose a month for analysis (for all months type all):   ')).lower()
            if month in months_options:
                break
            else:
                 print('')
                 print('Bad User...choose an AVAILABLE option')
                 print('Options:')
                 print('January, February, March, April, May, June, OR all')
        except:
            print('That is not a valid selection, Please choose again')
            print('Options:')
            print('January, February, March, April, May, June, OR all')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('The options for days are:')
    print('Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday')
    while True:
        try:
            day = str(input('Choose a weekday for analysis (for all months type all):   ')).lower()
            if day in weekday_options:
                break
            else:
                 print('')
                 print('Bad User...choose an AVAILABLE option')
                 print('Options:')
                 print('Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, OR all')
        except:
            print('That is not a valid selection, Please choose again')
            print('Options:')
            print('Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, OR all')

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
    # LOAD THE CSV
    df = pd.read_csv(CITY_DATA[city])

    #CSV loads Start time column in this format, from Excel Chicago.csv Cell C2: 6/23/2017  3:14:53 PM
    #CLEAN UP START TIME COLUMN TO PANDAS datetime
    #FROM HERE: https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #OUTPUT NO PARSEABLE WITH PANDAS, FORMAT IS :2017-06-23 03:14:53

    #Make new columns with datetime 
    #need months, weekday, hour, minute
    #https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.month.html
    df['Start_Time_Month']= df['Start Time'].dt.month
    df['Start_Time_Day']= df['Start Time'].dt.day_name()
    #day_name is a method
    df['Start_Time_Hour']= df['Start Time'].dt.hour
    df['Start_Time_Minute']= df['Start Time'].dt.minute

    #now that we have the above columns we can filter by them
    #FILTER MONTH
    if month in months:
        month_number= months.index(month)+1
        #+1, there is no 'zero' month ulike the index
        df = df[df['Start_Time_Month']==month_number]

    #now that we have the above columns we can filter by them
    #FILTER WEEKDAY
    if day in weekday:
        df = df[df['Start_Time_Day_Julian']==day.title()]
        #.title(), pandas dt.day_name outputs the first letter capitalized

    #print (df)
    return df


def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    #This method returns the time as a floating point number expressed in seconds since the epoch, in UTC.
    #Used for calculating the calculation speed.

    # display the most common month
    if month in months:
        print('You chose the month of %s' % month)
    else:
        mode_month = df['Start_Time_Month'].mode()[0]-1
        #-1, Shifting this back to an index of the months list
        print('The most common month for a ride is: %s' % months[mode_month].title())

    # display the most common day of week
    if day in weekday:
        print('You chose the day of %s' % day)
    else:
        mode_day = df['Start_Time_Day'].mode()[0]
        print('The most common weekday for a ride is: %s' % mode_day)

    # display the most common start hour
    mode_hour = df['Start_Time_Hour'].mode()[0]
    print('The most common hour of the day for a ride is: %s' % mode_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mode_start_station = df['Start Station'].value_counts().idxmax()
    print('Most Commonly used start station:', mode_start_station)

    # display most commonly used end station
    mode_final_station = df['End Station'].value_counts().idxmax()
    print('Most Commonly used ending station:', mode_final_station)

    # display most frequent combination of start station and end station trip
    Combo_Text= df['Start Station']+' and ending at '+df['End Station']
    Combo_Text_Answer = str(Combo_Text.mode().loc[0])
    print('The most common combination of station is starting at', Combo_Text_Answer)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('The TOTAL travel time is', total_time)

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('The AVERAGE travel time is', mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df ['User Type'].value_counts()
    print ('User Type breakdown by type:')
    print (user_types)
    print()
    print()

    # Display counts of gender
    if 'Gender' in df.columns:
       gender_types = df ['Gender'].value_counts()
       print ('User Type breakdown by Gender Data')
       print (gender_types)
    else:
        print ('User Type breakdown by Gender Data:')
        print ('No Gender Data to Report.')
        print()
        print()

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        year_of_birth = df['Birth Year']
        print ('User Type breakdown by Birth Year Data:')
        
        #EARLIEST BIRTH YEAR
        print ('The OLDEST User Was Born in the year:')
        print (str(year_of_birth.min()))

        #Youngest User
        print ('The YOUNGEST User Was Born in the year:')
        print (str(year_of_birth.max()))

        #Oldest User
        print ('The MOST COMMON year to be born in is:')
        print (str(year_of_birth.value_counts().idxmax()))
    
    else:
        print ('User Type breakdown by Birth Year Data:')
        print ('No Birth Year Data to Report.')
        print()
        print()


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def Display_Data(df, answer, iterator):
    print('Now we can show some DATA!')
    print('Would you like to see?')

    while answer != answers[1]:
        try:
            answer = str(input('answer:  ')).lower()
            if answer == answers[0]:
                print('Here are 5 lines of DATA')
                print('')
                print(df[iterator:iterator+5])
                #return answer
                iterator = iterator+5
                print('would you like to see more?')
                continue
                
            if answer == answers[1]:
                print('OK your\'re LOSS')
                return answer
                break

            else:
                print('That is not a valid answer, Please answer again')
                print('Options:')
                print('Yes, NO') 
                continue               
        except:
            print('That is not a valid answer, Please answer again')
            print('Options:')
            print('Yes, NO')   




def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        Display_Data(df,answer, iterator)



        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


###############-------LOOP-------##########################

if __name__ == "__main__":
	main()
