import pandas as pd
import re
def preprocess(data):

    if 'pm' in data:
         pattern = r'\d{2}/\d{2}/\d{2},\s\d{2}:\d{2}\s[ap]m\s-\s'
    else:
        pattern = r'\d{2}/\d{2}/\d{2},\s\d{2}:\d{2}\s-\s'
 
 
    dates = re.findall(pattern, data)
    messages = re.split(pattern, data)
    messages = messages[1:]

    df=pd.DataFrame(
        {
            'user_message':messages,
            'date':dates
        }
    )


    if 'pm' in data:
        df['date'] = df['date'].str.replace(' -','')
        df['date'] = pd.to_datetime(df['date'].str.strip(), format='%d/%m/%y, %I:%M %p', errors='coerce')
    else:
        df['date'] = pd.to_datetime(df['date'].str.strip(), format='%d/%m/%y, %H:%M -')



    def extract_user_message(text):
        match = re.findall(r"(.+?):(.*)", text)
        if match:
            return match[0]
        else:
            return ('Group Notification', text.strip())  
    df[['user', 'message']] = df['user_message'].apply(lambda x:extract_user_message(x)).apply(pd.Series)

    df.drop(columns=['user_message'], inplace=True)

    pattern = r'\d{2}/\d{2}/\d{2}, \d'
    df = df[~df['user'].str.contains(pattern, regex=True)]


    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute


    df['month_no']=df['date'].dt.month
    df['date_no']=df['date'].dt.date
    df['day_name']=df['date'].dt.day_name()


    return df