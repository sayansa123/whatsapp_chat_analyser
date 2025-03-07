import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns



# Function to show most common words
def show_most_common_words(df, person):
    st.title('Most Common Words')
    col1, col2 = st.columns(2)
    with col1:
        img = helper.create_wordCloud(df, person)
        if img is not None:
            fig, ax = plt.subplots()
            ax.imshow(img)
            st.pyplot(fig)
        else:
            st.warning("No valid words found to generate a word cloud.")
    with col2:
        x = helper.most_common_words(df, person)    
        if not x.empty:
            fig, ax = plt.subplots()
            ax.barh(x[0], x[1], color='red')
            st.pyplot(fig)
        else:
            st.warning("No common words found.")

# Function to show most common emojis
def show_most_common_emojis(df, person):
    st.title('Most Common Emojis')
    col1, col2 = st.columns(2)
    x = helper.emoji_analysis(df, person)
    with col1:
        fig, ax = plt.subplots()
        p = x['count'].head(10)
        q = x['emoji'].head(10)
        ax.pie(p, labels=q, autopct="%0.2f")
        st.pyplot(fig)
    with col2:
        st.table(x)

# Function to show timeline analysis
def show_timeline_analysis(df, person):
    st.title('Timeline Analysis')
    col1, col2 = st.columns(2)
    with col1:
        st.title('Monthly Timeline')
        temp = helper.monthly_timeline(df, person)
        fig, ax = plt.subplots()
        plt.plot(temp['time'], temp['message'], color='blue')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    with col2:
        st.title('Daily Timeline')
        temp = helper.daily_timeline(df, person)
        fig, ax = plt.subplots()
        plt.plot(temp['date_no'], temp['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

# Function to show activity analysis
def show_activity_analysis(df, person):
    st.title('Activity Analysis')
    col1, col2 = st.columns(2)
    with col1:
        st.title('Week Activity')
        temp = helper.week_activity(df, person)
        fig, ax = plt.subplots()
        ax.bar(temp['day_name'], temp['message'], color='#808080')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    with col2:
        st.title('Month Activity')
        temp = helper.month_activity(df, person)
        fig, ax = plt.subplots()
        ax.bar(temp['month'], temp['message'], color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


# Set page title and description
st.sidebar.title('WhatsApp Chat Analyser')
st.sidebar.markdown("""
    **WhatsApp Chat Analyzer**  
    Upload your WhatsApp chat export file to analyze message statistics, 
    most common words, emojis, and more.
""")

# Reset button to clear session state
if st.sidebar.button("Reset"):
    st.session_state.clear()  # Clear all session state
    st.rerun()  # Rerun the app (for Streamlit >= 1.27.0)

# File uploader
uploaded_file = st.sidebar.file_uploader("Choose a file", type=['txt'])
if uploaded_file is not None:
    try:
        # Read and preprocess the file
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocessor.preprocess(data)

        # Fetch unique users
        L = df['user'].sort_values().unique().tolist()
        if 'Group Notification' in L:
            L.remove('Group Notification')
        L.insert(0, 'Overall')
        person = st.sidebar.selectbox('Analysis wrt', L)

        # Add buttons for analysis
        if st.sidebar.button('Show Chats'):
            st.title('Chat Data')
            x = helper.dataframe(df, person)
            st.dataframe(x)

        if st.sidebar.button('Analyze'):
            st.title('Analysis Results')

            # Fetch stats
            no_messages, no_words, no_medias, no_links = helper.fetch_stats(df, person)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(label="Total Messages", value=no_messages)
            with col2:
                st.metric(label="Total Words", value=no_words)
            with col3:
                st.metric(label="Total Medias", value=no_medias)
            with col4:
                st.metric(label="Total Links", value=no_links)

            # Most active users
            st.title('Most Active Users')
            col1, col2 = st.columns(2)
            x, y = helper.fetch_most_active(df)
            with col1:
                fig, ax = plt.subplots()
                ax.bar(x['user'], x['no_message'], color='skyblue')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(y)

            # Most common words
            show_most_common_words(df, person)

            # Most common emojis
            show_most_common_emojis(df, person)

            # Timeline analysis
            show_timeline_analysis(df, person)

            # Activity analysis
            show_activity_analysis(df, person)

            # Heatmap
            st.title('Heat Map')
            user_heatmap = helper.heatmap(df, person)
            fig, ax = plt.subplots()
            sns.heatmap(user_heatmap, ax=ax)
            st.pyplot(fig)

            # Sentiment Analysis
            st.title('Sentiment Analysis')
            sentiment_df, sentiment_summary = helper.analyze_sentiment(df, person)
            col1, col2 = st.columns(2)
            with col1:
                st.header('Sentiment Distribution')
                fig, ax = plt.subplots()
                ax.pie(sentiment_summary['Count'], labels=sentiment_summary['Sentiment'], autopct="%0.2f%%", colors=['green', 'red', 'gray'])
                st.pyplot(fig)
            with col2:
                st.header('Sentiment Summary')
                st.dataframe(sentiment_summary)

    except Exception as e:
        st.error(f"An error occurred: {e}")