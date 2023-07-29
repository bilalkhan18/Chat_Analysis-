import streamlit as st
import preprocess
import helper
import matplotlib.pyplot as plt
from wordcloud import WordCloud
st.sidebar.title("Whatsapp Chat Analyzer")


uploaded_file = st.sidebar.file_uploader("Upload the file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    

    df = preprocess.preprocess(data)
    
    st.title("Top Statistics")
    st.divider()
    
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show Analysis WRT ",user_list)


    st.title("Sentiment Score of Chat")
    total_score= helper.calc_sentiment(selected_user,df)
    st.header(f"The Overall Sentiment Score of This Chat is: {total_score}")
    
    st.divider()
    


    if st.sidebar.button("Show Analysis"):
        
        num_messages, len_words = helper.fetch_stats(selected_user,df)

        

        col1, col2 = st.columns(2)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        
        with col2:
            st.header("Total Words")
            st.title(len_words)

        st.divider()

    st.title("Monthy Timeline")
    timeline = helper.timeline_func(selected_user,df)
    fig,ax = plt.subplots()
    ax.plot(timeline['Time'],timeline['message'],color="green")
    plt.xlabel("Month and Year")
    plt.ylabel("Number of messages")
    plt.xticks(rotation=90)
    st.pyplot(fig)       
    st.divider()

    st.title("Activity Map ")
    col1,col2 = st.columns(2)

    with col1:
        st.title("Most Active Days")
        daily_count = helper.daily_count(selected_user,df)
        fig,ax = plt.subplots()
        ax.bar(daily_count['index'],daily_count['day_name'],color="red")
        plt.xlabel("Day")
        plt.ylabel("Number of messages")
        plt.xticks(rotation=90)
        st.pyplot(fig)  

    with col2:
        st.title("Most Active Month")
        monthly_count = helper.monthly_count(selected_user,df)
        fig,ax = plt.subplots()
        ax.bar(monthly_count.index, monthly_count.values,color='orange')
        plt.xlabel("Month")
        plt.ylabel("Number of messages")
        plt.xticks(rotation=90)
        st.pyplot(fig)  




    if selected_user == "Overall":
        st.title("Most Active Users")
        most_active_users,percent_df = helper.active_users(df)
        fig, ax  = plt.subplots()
        

        col1,col2 = st.columns(2)

        with col1:
            ax.bar(most_active_users.index,most_active_users.values,color='red')
            plt.xticks(rotation=90)
            st.pyplot(fig)


        with col2:
            st.dataframe(percent_df)

    st.title("WordCloud")
    df_wc = helper.create_wordcloud(selected_user,df)
    fig,ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)


    emoji_df = helper.emoji_count(selected_user,df)
    st.title("Top Emojis used")
    col1,col2 = st.columns(2)

    with col1:
        st.dataframe(emoji_df)

    with col2:
        fig,ax = plt.subplots()
        ax.pie(emoji_df["Count"].head(),labels=emoji_df["Emoji"].head(),autopct="%0.2f")
        st.pyplot(fig)