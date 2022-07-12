from sklearn.utils import shuffle
import numpy as np
import pandas as pd
from scipy import stats

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
from sklearn.metrics import make_scorer, accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score

from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
import sklearn.metrics as metrics

# import plot libs
import math
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import HTML
import dataframe_image as dfi

import time
import pickle


# !pip install dataframe_image
# !pip install --upgrade pip
# !pip install selenium
# !pip install -U scikit-learn


# from selenium import webdriver
# driver = webdriver.Chrome("C:/Users/marti/Downloads/chromedriver_win32/chromedriver.exe")


rounds = 10
folds = 10
perc = "85"
path = "../models_result/" + perc + "/"


def t_stat_interpret(t):
    """
    Takes a scalar and returns a string with
    the css property `'color: yellow'` for queue values, white otherwise.
    """

    # degrees of freedom
    p = 0.05
    df = rounds - 1
    t_table = pd.read_csv("./t_distribution_table.csv")
    c = float(t_table.loc[df, str(round(p / 2, 3))])

    if t == "":
        color = 'white'
    else:
        # color = 'white' if t > c or t < -c else 'yellow'
        color = 'pink' if t > c or t < -c else 'lightgreen'
    return 'background: % s' % color


def scoring(pipeline, data, labels, iter):
    results_10CV = []

    # start iter
    for i in range(1, iter + 1):
        X, y = shuffle(data, labels, random_state=i * 42)
        results_10CV.append(np.mean(cross_val_score(estimator=pipeline,
                                                    X=X,
                                                    y=y,
                                                    cv=10,
                                                    n_jobs=-1
                                                    )))

    return results_10CV


# ------------------------ 10-fold cross validation ------------------------

def cross_validation(models, tweets, targets):
    # properties for new dataframe
    idx = (model['name'] for model in models)
    cols = ['Accuracy', 'Execution time', 'Std']
    cvs = pd.DataFrame(np.zeros((11, 3)), columns=cols, index=idx)
    # cm variable by the color palette from seaborn
    cm = sns.light_palette("seagreen", as_cmap=True)
    cs = sns.light_palette("royalblue", as_cmap=True)

    for model in models:
        start = time.time()

        model['pipeline'] = Pipeline(steps=[('vect', CountVectorizer(ngram_range=(1, 1))),
                                            ('tfidf', TfidfTransformer(smooth_idf=True, use_idf=True)),
                                            ('fselect', SelectPercentile(chi2, percentile=int(perc))),
                                            ('clf', model['fun'])])

        model['values'] = scoring(model['pipeline'], tweets, targets, rounds)

        end = time.time()

        cvs.loc[model['name']] = [float(("%.6f" % np.mean(model['values'])).rstrip('0').rstrip('.')), \
                                  str(round((end - start), 4)) + " s", \
                                  float("%.6f" % np.std(model['values']))]
        cvs.sort_values('Accuracy', inplace=True, ascending=False)

    print("\nCross validation results:\n")
    cvs.to_csv(path + "training_result_" + perc + "/cross_val_result.csv")

    cvs = cvs.style.background_gradient(cmap=cm, subset=['Accuracy']) \
        .background_gradient(cmap=cs, subset=['Std'])
    dfi.export(cvs, path + "training_result_" + perc + "/cross_val_result.png")
    display(HTML(cvs.to_html()))

    # discarded for execution time
    discarded = ["Bagging", "Random Forest", "Gradient Boosting"]
    # discarded for accuracy
    discarded.extend(["K Nearest", "Decision Tree", "Ada Boost", \
                      "Stochastic Gradient"])
    return discarded


# ----------------- t-test evaluation from library -------------------------

def t_test(models_selected):
    all_t_stat = []

    i = 0
    j = 0
    for model in models_selected:
        row = []
        i += 1
        j = 0
        for another_model in models_selected:
            j += 1
            if (j < i + 1):
                row.append("")
                continue
            t_statistic, p_value = stats.ttest_rel(model['values'], \
                                                   another_model['values'])
            # print(t_statistic, p_value)
            row.append(t_statistic)

        all_t_stat.append(row)

    print("\nT-test results:\n")

    ttest_matrix = pd.DataFrame(all_t_stat,
                                columns=(model['name'] for model in models_selected),
                                index=(model['name'] for model in models_selected))
    # delete empty column and row
    del ttest_matrix['Logistic Regression']
    ttest_matrix.drop(ttest_matrix.tail(1).index, inplace=True)

    ttest_matrix.to_csv(path + "training_result_" + perc + "/t_test_result.csv")
    ttest_matrix = ttest_matrix.style.applymap(t_stat_interpret)
    dfi.export(ttest_matrix, path + "training_result_" + perc + "/t_test_result.png")
    display(HTML(ttest_matrix.to_html()))

    discarded = []
    discarded.append("MultinomialNB")

    return discarded


# ---------------------- report and confusion matrix -----------------------

def get_report_conf_matrix(models, tweets, targets):
    print("\nReport and confusion matrix")

    for model in models:
        print(model['name'])
        predict = cross_val_predict(model['pipeline'], tweets, targets, cv=10)
        rep = metrics.classification_report(targets, predict,
                                            target_names=['0', '1'])
        print(rep)

        # save report
        rep = metrics.classification_report(targets, predict,
                                            target_names=['0', '1'], output_dict=True)
        df = pd.DataFrame(rep)
        df.to_csv(path + 'training_result_' + perc + '/' + model['name'] + '-report.csv')

        # calculate and print confusion matrix
        disp = ConfusionMatrixDisplay.from_predictions(
            targets,
            predict,
            values_format='g',
            display_labels=[0, 1],
            cmap=plt.cm.Blues
        )
        disp.ax_.set_title("Confusion matrix")

        print(disp.confusion_matrix)
        disp.figure_.savefig(path + 'training_result_' + perc + '/' + model['name'] + '-confusion_matrix.png')

        print("\n")


def train_models(data):
    data.sample(frac=1)

    tweets = data.text
    targets = data.target

    # models = name | fun | pipeline | values |
    models = [
        {"name": "Logistic Regression", "fun": LogisticRegression()},
        {"name": "SVM", "fun": svm.SVC()},
        {"name": "Decision Tree", "fun": DecisionTreeClassifier()},
        {"name": "MultinomialNB", "fun": MultinomialNB()},
        {"name": "Gradient Boosting", "fun": GradientBoostingClassifier()},
        {"name": "ComplementNB", "fun": ComplementNB()},
        {"name": "K Nearest", "fun": KNeighborsClassifier()},
        {"name": "Random Forest", "fun": RandomForestClassifier()},
        {"name": "Ada Boost", "fun": AdaBoostClassifier()},
        {"name": "Bagging", "fun": BaggingClassifier()},
        {"name": "Stochastic Gradient", "fun": SGDClassifier()}
    ]

    # analyze classifiers

    discarded = cross_validation(models, tweets, targets)

    models_selected = [s for s in models if s['name'] not in discarded]

    discarded = t_test(models_selected)

    models_selected = [s for s in models_selected if s['name'] not in discarded]

    get_report_conf_matrix(models, tweets, targets)

    # models building

    for model in models_selected:
        m = model['pipeline'].fit(tweets, targets)

        # save models
        filename = model['name'] + '.sav'
        pickle.dump(m, open(path + 'models_' + perc + '/' + filename, 'wb'))

    print("\nModels correctly saved!")


if __name__ == '__main__':
    pass