import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
nltk.download('punkt')


def remove_stopwords(tokens):
    nltk.download('stopwords')
    stop_words = set(stopwords.words('italian'))

    return [i for i in tokens if i not in stop_words]


def stem(tokens):
    # the stemmer requires a language parameter
    snow_stemmer = SnowballStemmer(language='italian')

    return [snow_stemmer.stem(word) for word in tokens]


def miningfull_words(stemmed):
    return [word for word in stemmed if len(word) > 2]


def textual(text):
    tweets = ""
    for word in text:
        tweets += word + " "

    return tweets


def remove_numbers(mean_words):
    return [word for word in mean_words if not word.isdigit()]


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


def elaborate(data):
    elaborated = []

    for index, tweet in data.iterrows():
        # print(tweet['text'])
        new_tweet = elaborating_steps(tweet['text']).strip()
        elaborated.append(new_tweet)
        data.at[index, 'text'] = new_tweet

    # print(elaborated)
    data = data.sort_values(by='datetime')

    print("Elaboration done")
    print("\n")

    return data


if __name__ == '__main__':
    pass
