from sklearn.utils import shuffle
import time
import numpy as np
import pandas as pd
from scipy import stats
import pickle

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.feature_selection import chi2, SelectPercentile

# import classifiers
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, BaggingClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn.neighbors import KNeighborsClassifier

# model selection and metrics
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import ConfusionMatrixDisplay

# import plot libs
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import HTML


perc = "85"
path = "../models_result/" + perc + "/"


def test_models(data):

    tweets = data['text']
    targets = data['target']

    models = [
        {"name": "Logistic Regression", "fun": LogisticRegression()},
        {"name": "SVM", "fun": svm.SVC()},
        {"name": "ComplementNB", "fun": ComplementNB()}
    ]

    # load the model from disk
    for model in models:

        loaded_model = pickle.load(open(path+'models_'+perc+'/'+model['name']+'.sav', 'rb'))
        print(model['name'])
        score = loaded_model.score(tweets, targets)
        print("Test score: {0:.2f} %".format(100 * score))
        y_predict = loaded_model.predict(tweets)

        rep = classification_report(targets, y_predict,
                                              target_names=['0', '1'])
        print(rep, '\n')

        # save reports
        rep = classification_report(targets, y_predict,
                                    target_names=['0', '1'], output_dict=True)
        df = pd.DataFrame(rep).transpose()
        df.to_csv(path+'test_result_'+perc+'/'+model['name']+'-report.csv')
