from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import emoji
from collections import Counter

def dataframe(df, person):
    if(person!='Overall'):
        df = df[df['user']==person]
    return df

def fetch_stats(df, person):
    if(person!='Overall'):
        df = df[df['user']==person]    
    no_messages = df.shape[0]       # total messages   
    L=[]
    for i in df['message']:
        L.extend(i.split())
    no_words = len(L)               # total words
    no_media = df[df['message']==' <Media omitted>'].shape[0]   # total medias  
    extracter = URLExtract()
    links =[]
    for i in df['message']:
        links.extend(extracter.find_urls(i))    # total links
    no_links = len(links)
    return no_messages,no_words, no_media, no_links

def fetch_most_active(df):
    x = df['user'].value_counts().head(5).reset_index().rename(columns={'count':'no_message'})  # most active user
    y = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'count':'percentage'}) # percentage of messages
    return x,y

def create_wordCloud(df,person):
    if(person!='Overall'):
        df = df[df['user']==person]

    temp = df[df['user']!='Group Notification']
    temp = temp[temp['message']!=' <Media omitted>']
    temp = temp[temp['message']!=' This message was deleted']

    with open ('stop_words_english.txt', 'r') as f:
        stop_words = f.read()

    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    temp['message']=pd.DataFrame(words)

    wc = WordCloud(width=500, height=500, background_color='white')
    img = wc.generate(temp['message'].str.cat(sep=" "))
    return img

def most_common_words(df,person):
    if(person!='Overall'):
        df = df[df['user']==person]
   
    temp = df[df['user']!='Group Notification']
    temp = temp[temp['message']!=' <Media omitted>']
    temp = temp[temp['message']!=' This message was deleted']

    with open ('stop_words_english.txt', 'r') as f:
        stop_words = f.read()

    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    from collections import Counter
    x = pd.DataFrame(Counter(words).most_common(10))
    x.sort_values(by = 1, ascending=True, inplace=True)
    return x

def emoji_analysis(df,person):
    if(person!='Overall'):
        df = df[df['user']==person]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_counts = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=['emoji', 'count'])
    x = emoji_counts.head(10)
    return x

def monthly_timeline(df, person):
    if(person!='Overall'):
        df = df[df['user']==person]
    temp = df.groupby(['year','month','month_no'])['message'].count().reset_index()
    L = []
    for i in range(temp.shape[0]):
        L.append(str(temp['year'][i]) + "-" + str(temp['month'][i]))
    temp['time']=L
    temp = temp.sort_values(['year','month_no'],ascending=[True,True])
    return temp

def daily_timeline(df, person):
    if(person!='Overall'):
        df = df[df['user']==person]
    temp = df.groupby(['date_no'])['message'].count().reset_index()
    return temp

def week_activity(df,person):
    if(person!='Overall'):
        df = df[df['user']==person]
    temp = df.groupby(['day_name'])['message'].count().reset_index()
    return temp

def month_activity(df,person):
    if(person!='Overall'):
        df = df[df['user']==person]
    temp = df.groupby(['month'])['message'].count().reset_index()
    return temp

def heatmap(df,person):
    if(person!='Overall'):
        df = df[df['user']==person]
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap