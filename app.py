import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns

st.sidebar.title('WhatsApp Chat Analyser')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data =bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    

    # Fetch Unique Users
    L = df['user'].sort_values().unique().tolist()
    L.remove('Group Notification')
    L.insert(0,'Overall')
    person = st.sidebar.selectbox('Analysis wrt ',L)
    
    # Add button
    button = st.sidebar.button('Chats')
    if button:
        x = helper.dataframe(df,person)
        st.dataframe(x)

        
    # Add button
    button = st.sidebar.button('Analysis')
    if button:
        no_messages, no_words, no_medias, no_links = helper.fetch_stats(df,person)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header('Total Messages')
            st.title(no_messages)
        with col2:
            st.header('Total Words')
            st.title(no_words)
        with col3:
            st.header('Total Medias')
            st.title(no_medias)
        with col4:
            st.header('Total Links')
            st.title(no_links)

        col1, col2 = st.columns(2)
        x,y = helper.fetch_most_active(df)
        with col1:
            st.title('Most Active Users')
            name = x.user
            no_message = x.no_message
            fig,ax = plt.subplots()
            plt.bar(name,no_message)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.title('Percentages of Messages')
            st.dataframe(y)


        st.title('Most Common Words')
        col1, col2 = st.columns(2)
        with col1:
            img = helper.create_wordCloud(df,person)
            fig,ax = plt.subplots()
            ax.imshow(img)
            st.pyplot(fig) 
        with col2:
            x = helper.most_common_words(df, person)    
            fig,ax = plt.subplots()
            ax.barh(x[0],x[1], color='red')
            st.pyplot(fig)
        # with col3:
        #     y = helper.most_common_words(df, person)
        #     y.sort_values(by = 1, ascending=False, inplace=True)
        #     st.dataframe(y)
        

        st.title('Most Common Emoji')
        col1, col2 = st.columns(2)
        x = helper.emoji_analysis(df, person)
        with col1:
            fig,ax = plt.subplots()
            p = x['count'].head(10)
            q = x['emoji'].head(10)
            ax.pie(p, labels=q, autopct="%0.2f")
            st.pyplot(fig)
        with col2:
            st.table(x)
            
        
        col1, col2 = st.columns(2)
        with col1:
            st.title('Monthly timeline')
            temp = helper.monthly_timeline(df, person)
            fig,ax = plt.subplots()
            plt.plot(temp['time'], temp['message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.title('Daily timeline')
            temp = helper.daily_timeline(df, person)
            fig,ax = plt.subplots()
            plt.plot(temp['date_no'], temp['message'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        col1, col2 = st.columns(2)
        with col1:
            st.title('Week Activity')
            temp = helper.week_activity(df, person)
            fig,ax = plt.subplots()
            ax.bar(temp['day_name'], temp['message'], color='#808080')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.title('Month Activity')
            temp = helper.month_activity(df, person)
            fig,ax = plt.subplots()
            ax.bar(temp['month'], temp['message'], color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        st.title('Heat Map')
        user_heatmap = helper.heatmap(df, person)
        fig,ax = plt.subplots()
        sns.heatmap(user_heatmap)
        st.pyplot(fig)