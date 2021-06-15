import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns
import re
import string
from textanalytics import get_insights
from mywordcloud import generate_wordcloud

selected_columns = ["Review Text","sentiment_overall",
"emotional_traits","behavioral_traits"]

selected_columns_tweets = ["text","sentiment_overall",
"emotional_traits","behavioral_traits"]

strategy = st.sidebar.radio("Select Analysis Strategy",
                 ('Tweets','Customer Reviews','Single Input'))

def clean_text(text):
    '''Make text lowercase,remove punctuation
    .'''
    text = text.strip()
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\[', '', text)
    text = re.sub('\]', '', text)
    return text

def display_category(filename,
selected_columns =selected_columns,
age_flag = True,
colname_text = "Review Text",
handle =""):

    df = pd.read_csv(filename)
    df["emotional_traits"] = df["emotional_traits"].fillna("")
    df["behavioral_traits"] = df["behavioral_traits"].fillna("")

    topic = "# " + str(select_event)
    if sentiment_cat == "Positive only":
        df = df[df["sentiment_overall"] > 0]
        topic = "# " + str(sentiment_cat) + " " + str(select_event)
    elif sentiment_cat == "Negative only":
        df = df[df["sentiment_overall"] < 0]
        topic = "# " + str(sentiment_cat) + " " + str(select_event)
    
    if emotions == "All":
        pass 
    else:
        df = df[df["emotional_traits"] == emotions]

    if behavior == "All":
        pass 
    else:
        df = df[df["behavioral_traits"] == behavior]
    
    if handle == "" or handle == "All":
        pass
    else:
        df = df[df["handle"] == handle]

    if(len(df) == 0):
        st.markdown("**No records** found matching the criteria. \
        Please select another criteria")
        return

#########################################################################################

    st.markdown(topic)
    st.markdown("## Distribution of sentiments")

    fig = Figure()
    ax = fig.subplots()
    sns.histplot(df["sentiment_overall"],ax=ax, kde=True)
    st.pyplot(fig)

    st.table(df["sentiment_overall"].describe())
#########################################################################################
    data_group = df["emotional_traits"].value_counts().reset_index().head(10)
    some_values = [""]
    data_group = data_group.loc[~data_group['index'].isin(some_values)]

    if len(data_group) > 0:
        st.markdown("## Distribution of emotional traits")
        st.table(data_group)

        fig = Figure()
        ax = fig.subplots()
        sns.barplot(x = data_group['emotional_traits'],
        y = data_group['index'],
        color="blue",ax = ax)
        st.pyplot(fig)

#########################################################################################

    data_group = df["behavioral_traits"].value_counts().reset_index().head(10)
    some_values = [""]
    data_group = data_group.loc[~data_group['index'].isin(some_values)]
    
    if len(data_group) > 0:
        st.markdown("## Distribution of behavioral traits")
        st.table(data_group)

        fig = Figure()
        ax = fig.subplots()
        sns.barplot(x = data_group['behavioral_traits'], 
        y = data_group['index'],
        color="goldenrod",ax = ax)
        st.pyplot(fig)

#########################################################################################
    st.markdown("## Most Important Concepts")
    concepts_all = []
    index_values = df.index.values
    
    concepts_all = ""
    index_values = df.index.values
    
    for i in index_values:
        for item in df.loc[[i],["concepts"]]["concepts"]:
            concepts_all = concepts_all +  item + ","
    concepts_all = concepts_all.split(",")
    concepts_all_df = pd.DataFrame({'concepts':concepts_all})
    concepts_all_df["concepts"] = concepts_all_df["concepts"].apply(lambda x:clean_text(x))
    
    
    data_group = concepts_all_df["concepts"].value_counts().reset_index().head(10)
    some_values = [""]
    data_group = data_group.loc[~data_group['index'].isin(some_values)]

    st.table(data_group)

    fig = Figure()
    ax = fig.subplots()
    sns.barplot(x = data_group['concepts'], 
    y = data_group['index'],
     color="black",ax = ax)
    st.pyplot(fig)
#########################################################################################

    if age_flag:
        st.markdown("## Distribution of Age")

        fig = Figure()
        ax = fig.subplots()
        sns.histplot(df["Age"],ax=ax, kde=True)
        st.pyplot(fig)

        st.table(df["Age"].describe())
#########################################################################################
    st.markdown("## Most Common Words")
    generate_wordcloud(filename,colname_text)

    if sentiment_cat == "Positive only":
        sort_flag = False
        topic_senti= "## Most positive reviews"
    elif sentiment_cat == "Negative only" or sentiment_cat == "All":
        sort_flag = True
        topic_senti= "## Most negative reviews"

    st.markdown(topic_senti)

    st.table(df.sort_values(by=["sentiment_overall"],
                ascending = sort_flag)[selected_columns][:num_rows])
#########################################################################################
if strategy == "Tweets":
    select_event =""
    st.sidebar.markdown("## Select Handle")
    select_handle = st.sidebar.selectbox('Please choose Twitter handle?',
                                        [ 
                                        'All', 
                                        'HillaryClinton', 
                                        'realDonaldTrump'])
    st.title("Tweets analysis for " + select_handle)

if strategy == "Customer Reviews":
    st.title("Women's clothing reviews")
    st.sidebar.markdown("## Select Category")
    select_event = st.sidebar.selectbox('How do you want to find data?',
                                        [ 
                                        'Dresses', 
                                        'Pants', 
                                        'Swim',  
                                        'Jeans',
                                        'Blouses',
                                        'Intimates' ])

if ((strategy == "Customer Reviews") or (strategy == "Tweets")):

    # Add a slider to the sidebar:
    num_rows = st.sidebar.slider('Number of rows to display',0, 100, 20)

    sentiment_cat = st.sidebar.selectbox("Select sentiment category",
                    ['All', 'Positive only', 'Negative only'])

    emotions = st.sidebar.selectbox('Emotions ',
    ['All','Sadness','Torment','Suffering','Sorrow',
'Disappointment','Disillusion','Resignation',
'Surprise','Happiness','Excitement','Joy',
'Amusement','Well-Being','Satisfaction','Relief'])

    behavior = st.sidebar.selectbox("Behavior",['All','Sedentariness',
        'Passivity',
        'Calmness',
        'Initiative',
        'Dynamism',
        'Rejection',
        'Apathy',
        'Apprehension',
        'Traditionalism',
        'Conformism',
        'Negativity',
        'Bias','Cautiousness',
        'Progressiveness',
        'Acceptance',
        'Courage',
        'Positivity',
        'Curiosity'])
else:
    select_event = ""
    user_input = st.text_area("Your Input",
    """Very nice fabric but disappointed in the stitching on the knees it looks nice but makes the pants very uncomfortable and tight around the knees  too bad because i love the style and hoped they would work""")

    result = st.button("Get Text Analytics")

    if result:
        insights = get_insights(user_input)
        st.markdown("# Overall Sentiment")
        st.markdown(insights.sentiments)
       
        st.markdown("# Emotions")
        st.markdown(insights.emotions)

        st.markdown("# Behaviour")
        st.markdown(insights.behavior)

        st.markdown("# Key Phrases")
        st.write(insights.keyphrases)

        st.markdown("# Key Entities")
        st.write(insights.keyentities)

        st.markdown("# Key Relations")
        st.markdown(insights.keyrelationsrelated, unsafe_allow_html=True)



#########################################################################################
if select_event == 'Intimates':
    display_category(filename = "output/intimates_sentiment_traits.csv")
elif select_event == 'Dresses':
    display_category(filename = "output/dress_sentiment_traits.csv")
elif select_event == 'Jeans':
    display_category(filename = "output/jeans_sentiment_traits.csv")
elif select_event == 'Pants':
    display_category(filename = "output/pants_sentiment_traits.csv")
elif select_event == 'Swim':
    display_category(filename = "output/swim_sentiment_traits.csv")
elif select_event == 'Blouses':
    display_category(filename = "output/blouses_sentiment_traits.csv")
#########################################################################################
if strategy == "Tweets":
    display_category(filename="output/tweets_analysis.csv",
    selected_columns =selected_columns_tweets,
    age_flag = False,
    colname_text = "text",handle = select_handle)




