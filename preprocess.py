import re
import pandas as pd

def preprocess(data):
    pattern =  r'\[\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}:\d{2} [APapMm]{2}\]'
    message = re.split(pattern,data)
    dates = re.findall(pattern,data)

    message.remove("")
    df = pd.DataFrame({'user_message':message, 'message_date':dates})

    df["message_date"] = pd.to_datetime(df["message_date"],format="[%d/%m/%y, %I:%M:%S %p]")


    df.rename(columns={'message_date':'date'},inplace=True)


    users = []
    messages = []
    for message in df["user_message"]:
        entry = re.split('([\w\W]+?):\s',message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        
        else:
            users.append("Group_Notification")
            messages.append(entry[0])
        
    df['user'] = users 
    df["message"] = messages
    
    df.drop('user_message',axis=1,inplace=True)
    df['date'].dt.year
    df['year'] = df['date'].dt.year
    df["month"] = df["date"].dt.month_name()
    df["day"] = df["date"].dt.day
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute

    return df