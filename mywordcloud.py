import numpy as np
import pandas as pd
import re
import nltk
import string
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

COLNAME ="Review Text"
NEWCOLNAME = COLNAME + "_"

PUNCT_TO_REMOVE = string.punctuation
def remove_punctuation(text):
    text = str(text)
    """custom function to remove the punctuation"""
    return text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))

nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
", ".join(stopwords.words('english'))

STOPWORDS = set(stopwords.words('english'))
def remove_stopwords(text):
    
    text = str(text)
    """custom function to remove the stopwords"""
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])

from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()
def stem_words(text):
    
    text = str(text)
    return " ".join([stemmer.stem(word) for word in text.split()])

from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
def lemmatize_words(text):
    text = str(text)
    return " ".join([lemmatizer.lemmatize(word) for word in text.split()])



def generate_wordcloud(filename,COLNAME = COLNAME):
    df = pd.read_csv(filename)


    df[COLNAME + "_"] = df[COLNAME].apply(lambda text: remove_punctuation(text))
    df[COLNAME + "_"] = df[COLNAME + "_"].apply(lambda text: remove_stopwords(text))

    X = df[COLNAME + "_"]
    from collections import Counter
    cnt = Counter()
    for text in X.values:
        for word in text.split():
            cnt[word] += 1

    df = pd.DataFrame.from_dict(cnt, orient='index').reset_index()
    df = df.rename(columns={'index':'words', 0:'count'})

    fig = Figure()
    ax = fig.subplots()
    df = df.sort_values(by=['count'],ascending = False)
    df = df.head(20)

    sns.barplot(x = df['count'],
    y = df['words'],
     color="black",ax = ax)
    st.pyplot(fig)
    
    text =' '.join(df["words"])
    wordcloud = WordCloud(max_words=len(text),
    max_font_size=40).generate(text)

    fig, ax = plt.subplots()

    # Display the generated image:
    ax.imshow(wordcloud)
    ax.axis("off")
    plt.show()
    st.pyplot(fig)
    