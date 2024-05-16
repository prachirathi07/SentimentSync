from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

# Initialize URL extractor
extract = URLExtract()

def fetch_stats(selected_user, df):
    # Filter data for the selected user if not 'Overall'
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Number of messages
    num_messages = df.shape[0]
    # Total words
    words = [word for message in df['message'] for word in message.split()]
    # Number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    # Extract URLs
    links = [link for message in df['message'] for link in extract.find_urls(message)]

    return num_messages, len(words), num_media_messages, len(links)

def create_wordcloud(selected_user, df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = set(f.read().split())

    # Filter data for the selected user if not 'Overall'
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter out group notifications and media messages
    temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>\n')]

    # Function to remove stop words from messages
    def remove_stop_words(message):
        return " ".join([word for word in message.lower().split() if word not in stop_words])

    # Generate word cloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = set(f.read().split())

    # Filter data for the selected user if not 'Overall'
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter out group notifications and media messages
    temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>\n')]

    # Count most common words excluding stop words
    words = [word for message in temp['message'] for word in message.lower().split() if word not in stop_words]
    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Frequency'])
    return most_common_df

def emoji_helper(selected_user, df):
    # Filter data for the selected user if not 'Overall'
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Extract emojis from messages
    emojis = [c for message in df['message'] for c in message if c in emoji.EMOJI_DATA]
    emoji_df = pd.DataFrame(Counter(emojis).most_common(), columns=['Emoji', 'Count'])
    return emoji_df

def week_activity_map(selected_user, df):
    # Filter data for the selected user if not 'Overall'
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Count messages by day of the week
    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    # Filter data for the selected user if not 'Overall'
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Count messages by month
    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    # Filter data for the selected user if not 'Overall'
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Create heatmap data
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap
