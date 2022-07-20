import os

import pandas as pd
import numpy as np
import datetime
import pickle
import string
import time
import preprocessing
import BSblocker

from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import ComplementNB
from sklearn.metrics import classification_report
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.feature_selection import chi2, SelectPercentile
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


# ## - Extract peaks


def extract_peak(input_file, peak_date, output_file):       # es. peak_date = 2002-03-10

    df = pd.read_csv(input_file, index_col=False, delimiter=",")

    end_peak = peak_date+' 23:59:59+00:00'
    start_peak = peak_date+' 00:00:00+00:00'
    peak = df[(df['datetime'] > start_peak) & (df['datetime'] < end_peak)]

    peak.to_csv('./retrain/'+output_file, index=False, sep=',')

    print("Peaks extracted ")


# # Concept drift

# ## - Training

def cd_training(path, data, i):
    print("Training...")

    tweets = data.text
    targets = data.target

    model = {'name': 'ComplementNB', 'fun': ComplementNB()}

    # model building
    model['pipeline'] = Pipeline(steps=[('vect', CountVectorizer(ngram_range=(1, 1))),
                                        ('tfidf', TfidfTransformer(smooth_idf=True, use_idf=True)),
                                        ('fselect', SelectPercentile(chi2, percentile=85)),
                                        # ('fselect', SelectKBest(chi2, k='all')),
                                        ('clf', model['fun'])])

    m = model['pipeline'].fit(tweets, targets)

    print("Number of features: ", len(model['pipeline']['vect'].vocabulary_))

    # save model
    filename = model['name'] + '_interval' + str(i) + '.sav'
    pickle.dump(m, open(path + '/' + filename, 'wb'))

    print("\nModel correctly saved!\n")
    print('─' * 10)


# ## - Create window


def create_window(i, file1, file2):

    print("Creating window...")
    df1 = pd.read_csv(file1, index_col=False, delimiter=",")
    df1.sort_values('datetime', inplace=True, ascending=True)
    print("Previous window: ", df1.shape)

    data2 = pd.read_csv(file2, index_col=False, delimiter=",")
    data2.sort_values('datetime', inplace=True, ascending=True)
    print("New tweets: ", data2.shape)


    window = pd.concat([df1, data2])
    print("New window: ", window.shape)

    window_name = './retrain/interval' + str(i) + '.csv'
    window.to_csv(window_name, index=False)

    return window_name, window


# ## - Get files for building a new window

def get_files(i):

    j = i-1
    list = []
    list.append('./retrain/interval' + j + '.csv')
    list.append('./retrain/interval' + i + '.csv')

    return list


def incremental_cd(model):

    print("\n*********** INCREMENTAL MODEL ************\n")

    i = 6

    # create window
    list = get_files(i)  # old and new tweets
    print("Files to merge: ", list)
    file1 = list[0]
    file2 = list[1]

    interval_name, interval = create_window(i, file1, file2)
    print("File created: ", interval_name, "\n")

    # train
    training_data = preprocessing.preprocess(interval)
    training_data = preprocessing.elaborate(training_data)

    cd_training(training_data, i)


# ## - Concept drift main


def predict(date, username, tweet, output_file, text, mylist):

    list = []
    list.append(tweet)

    model = {"name": "ComplementNB", "fun": ComplementNB()}

    # incremental_cd(model)

    loaded_model = pickle.load(open(model['name'] + '.sav', 'rb'))

    predicted = loaded_model.predict(list)

    df = pd.DataFrame([[date, text, username, predicted[0]]], columns=['datetime', 'text', 'username', 'target'])
    if not os.path.isfile("./predicted/" + output_file):
        df.to_csv("./predicted/" + output_file, header='column_names', index=False)
    else:  # else it exists so append without writing the header
        df.to_csv("./predicted/" + output_file, mode='a', header=False, index=False)

    print(predicted, tweet)
    if predicted == 1:
        BSblocker.show_users(username, mylist)


def main():
    pass

if __name__ == "__main__":
    main()