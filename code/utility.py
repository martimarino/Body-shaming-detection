import csv
import pandas as pd
import glob
import os
import re

input_file = '../labeled/12-01-rebalanced.csv'
output_file = '../labeled/12-01-labeled.csv'


def details():
    tot0 = len(df[df.target == '0'])
    tot1 = len(df[df.target == '1'])

    print(df.shape)

    print("Tot: ", tot0 + tot1, "(0: ", tot0, ", 1: ", tot1, ")")


def extractLabeled(df):
    labeled = df[(df.target == '0') | (df.target == '1')]
    labeled = labeled.sort_values('Datetime')
    labeled.to_csv(output_file, index=False, sep=',')

def concat():
    # setting the path for joining multiple files
    files = os.path.join("../monitoring/", "*.csv")

    # list of merged files returned
    files = glob.glob(files)

    print("Resultant CSV after joining all CSV files at a particular location...");

    # joining files with concat and read_csv
    df = pd.concat(map(pd.read_csv, files), ignore_index=True)
    df.sort_values('datetime', inplace=True, ascending=True)
    print(df.shape)

    df.to_csv('../merged/monitoring.csv', index=False, sep=',')


if __name__ == '__main__':
    df = pd.read_csv(output_file, index_col=False, delimiter=",")
    # extractLabeled(df)
    details()
