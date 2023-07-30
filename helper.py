
from wordcloud import WordCloud
from collections import Counter
import emoji
import pandas as pd
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer 
def fetch_stats(selected_user,df):
    

    if selected_user != "Overall":
        df =  df[df['user']==selected_user]


    words = []
    for message in df['message']:
        words.extend(message.split())    

    num_messages = df.shape[0]    
       

    return num_messages, len(words)
   

def active_users(df):
    five_active_users = df['user'].value_counts().head()
    percent_df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return five_active_users,percent_df



def clear_message(df):

    
    def clear(x):
        if "image omitted" in x:
            return " "
        if "audio omitted" in x:
            return " "
        if "document omitted" in x:
            return " "
        return x

    temp = df
    temp["message"] = temp['message'].apply(clear)    
    return temp


def create_wordcloud(selected_user,df):


    temp = clear_message(df)
    if selected_user != "Overall":
        df =  df[df['user']==selected_user]

    wc = WordCloud(width=500,height=500,background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def emoji_count(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user']==selected_user]

    emoji_list = []
    for message in df['message']:
        emoji_list.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emoji_list).most_common(len(Counter(emoji_list))))
    emoji_df.columns = ["Emoji","Count"]

    return emoji_df 


def timeline_func(selected_user,df):
        if selected_user != "Overall":
            df = df[df['user']==selected_user]

        df['month_num'] = df['date'].dt.month    
        timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()

        time = []
        for i in range(timeline.shape[0]):
            time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
        timeline["Time"] = time

        return timeline


def daily_count(selected_user,df):
        if selected_user != "Overall":
            df = df[df['user']==selected_user]

          
        
        return df['day_name'].value_counts()

def monthly_count(selected_user,df):
        if selected_user != "Overall":
            df = df[df['user']==selected_user]

        return df['month'].value_counts()



def calc_sentiment(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user']==selected_user]
    sid = SentimentIntensityAnalyzer()
    df['scores'] = df['message'].apply(lambda message: sid.polarity_scores(message))
    df['compound']  = df['scores'].apply(lambda score_dict: score_dict['compound'])
    return round((df['compound'].sum()/df.shape[0])*100,2)



    

