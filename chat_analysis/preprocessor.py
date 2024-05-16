import re
import pandas as pd

def preprocess(data):
    # Regular expression patterns to extract datetime and split messages
    datetime_pattern = r'\[\d{2}/\d{2}/\d{2},\s\d{2}:\d{2}:\d{2}\]'
    message_pattern = r'\[\d{2}/\d{2}/\d{2},\s\d{2}:\d{2}:\d{2}\]\s*'

    # Extract dates using regex
    dates = re.findall(datetime_pattern, data)
    dates = [date.strip('[]') for date in dates]  # Remove square brackets

    # Split data into individual messages
    messages = re.split(message_pattern, data)[1:]  # Skip the first split as it might be empty

    # Create a DataFrame from the extracted data
    df = pd.DataFrame({'message_date': dates, 'user_message': messages})

    # Convert message_date from string to datetime object
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M:%S')

    # Rename 'message_date' column to 'date'
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Initialize lists for users and actual messages
    users = []
    actual_messages = []

    for message in df['user_message']:
        # Split each message into user and message part
        entry = re.split('([\w\W]+?):\s', message)
        if len(entry) > 1:  # If a user is identified
            users.append(entry[1])
            actual_messages.append(entry[2])
        else:  # If it's a group notification
            users.append('group_notification')
            actual_messages.append(entry[0])

    # Add extracted users and messages to the DataFrame
    df['user'] = users
    df['message'] = actual_messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract additional datetime information
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    df['period'] = df['hour'].apply(lambda x: f"{x:02d}-{(x + 1) % 24:02d}")


    return df
