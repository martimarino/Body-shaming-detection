import pandas as pd
from preprocessing import preprocess
from elaboration import elaborate
from model_training import train_models
from sklearn.feature_extraction.text import CountVectorizer


def train():

    training_set_file = 'labeled/12-01-rebalanced-only-labeled.csv'
    train_data = pd.read_csv(training_set_file, index_col=False, delimiter=",")

    train_data = preprocess(train_data)
    train_data = elaborate(train_data)

    # print(train_data.shape)
    #tot0 = len(train_data[train_data.target == '0'])
    #tot1 = len(train_data[train_data.target == '1'])

    train_models(train_data)


def test():

    test_set_file = './labeled/2022-02-labeled-only.csv'
    test_data = pd.read_csv(test_set_file, index_col=False, delimiter=",")

    test_data = preprocess(test_data)
    test_data = elaborate(test_data)

    # print(test_data.shape)
    # tot0 = len(train_data[test_data.target == '0'])
    # tot1 = len(train_data[test_data.target == '1'])

    test_models(test_data)


if __name__ == '__main__':
    train()
    test()
    pass