# # Clean data

import re
import string

import nltk
import pandas as pd

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize

import predict_retrain


def clean(tweet):
    dfk = pd.read_csv("./keys.txt", sep=';')
    Words = dfk['Words'].values

    # remove URLs and mentions
    tweet = re.sub(r'(?:@|https?://)\S+', '', tweet, flags=re.MULTILINE)

    # remove new lines
    if tweet.endswith("\n") or tweet.endswith("\r"):
        tweet = tweet.replace("\n", "").replace("\r", "")
    else:
        tweet = tweet.replace("\n", " ").replace("\r", " ")

    # remove multiple spaces
    tweet = re.sub('\\s+', ' ', tweet)

    # remove tweets without keywords
    for word in Words:
        if word in tweet.lower():
            return tweet
    return ""


# # Preprocessing

# ## - Remove punctuation marks, brackets, quotes, special characters

def remove_punctuation(text):
    text = "".join([i for i in str(text) if i not in string.punctuation])
    text = text.replace('\u201D', " ")
    text = text.replace('\u2018', " ")
    text = text.replace('\u2019', " ")
    text = text.replace('\u201c', " ")
    text = text.replace('\u2026', " ")
    text = re.sub(r'\.{2,}', ' ', text)

    return text


# ## - Text reformat

def text_reformat(text):
    # remove two or more dots
    text = re.sub(r'\.{2,}', ' ', text)
    # remove two or more letters: { bellooooo -> bello}
    text = re.sub(r'(.)\1+', r'\1\1', text)

    return text.lower()


# ## - Remove emoticons

def remove_emojis(data):
    emoj = re.compile("["
                      u"\U0001F600-\U0001F64F"  # emoticons
                      u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                      u"\U0001F680-\U0001F6FF"  # transport & map symbols
                      u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                      u"\U00002500-\U00002BEF"  # chinese char
                      u"\U00002702-\U000027B0"
                      u"\U00002702-\U000027B0"
                      u"\U000024C2-\U0001F251"
                      u"\U0001f926-\U0001f937"
                      u"\U00010000-\U0010ffff"
                      u"\u2640-\u2642"
                      u"\u2600-\u2B55"
                      u"\u200d"
                      u"\u23cf"
                      u"\u23e9"
                      u"\u231a"
                      u"\ufe0f"  # dingbats
                      u"\u3030"
                      "]+", re.UNICODE)

    return re.sub(emoj, '', data)


# ## - Preprocessing call

def preprocessing_steps(data):
    new_data = remove_punctuation(data)
    new_data = text_reformat(new_data)
    new_data = remove_emojis(new_data)

    return new_data


def preprocess(data):

    data = preprocessing_steps(data)

    print("Preprocessing done")
    print("\n")

    return data


# # Elaboration

# ## - Stopwords removal

def remove_stopwords(tokens):
    nltk.download('stopwords')
    stop_words = set(stopwords.words('italian'))

    return [i for i in tokens if i not in stop_words]


# ## - Stemming

def stem(tokens):
    # the stemmer requires a language parameter
    snow_stemmer = SnowballStemmer(language='italian')

    return [snow_stemmer.stem(word) for word in tokens]


# ## - Remove miningless words

def miningfull_words(stemmed):
    return [word for word in stemmed if len(word) > 2]


# ## - Remove features with numbers

def remove_numbers(mean_words):
    return [word for word in mean_words if not word.isdigit()]


# ## - Elaboration call

def elaborating_steps(t):
    # print(t)

    tokens = word_tokenize(t)
    # print(tokens)
    tokens = remove_stopwords(tokens)
    # print(tokens)
    stemmed_words = stem(tokens)
    # print(stemmed_words)
    mean_words = miningfull_words(stemmed_words)
    # print(mean_words)
    numbers_removed = remove_numbers(mean_words)
    # print(numbers_removed)
    # print("\n")

    elaborated_tweet = ""
    for word in numbers_removed:
        elaborated_tweet += word + " "

    return elaborated_tweet


def elaborate(tweet):
    new_tweet = elaborating_steps(tweet).strip()

    print("Elaboration done")
    print("\n")

    return new_tweet


def prep(date, username, data, output_file, mylist, started):
    text = data
    data = preprocess(data)
    data = elaborate(data)
    predict_retrain.predict(date, username, data, output_file, text, mylist, started)

def main():
    pass

if __name__ == "__main__":
    main()