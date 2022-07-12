import pandas as pd
import random
from colorama import Fore, Style

file = '2022-05-labeled.csv'


def count(df):

    tot0 = len(df[df.target == '0'])
    tot1 = len(df[df.target == '1'])

    print("Tot: ", tot0 + tot1, "(0: ", tot0, ", 1: ", tot1, ")")


def createDict(df):

    df0 = df[(df.target == '0')]
    df1 = df[(df.target == '1')]

    for word in Words:
        stat[word + "0"] = df0.text.str.contains(word).sum()
        stat[word + "1"] = df1.text.str.contains(word).sum()

    print(Fore.CYAN + " ")
    count(df)
    print(stat)
    print(Style.RESET_ALL)


if __name__ == '__main__':

    df = pd.read_csv(file, index_col=False, delimiter=",")
    dfk = pd.read_csv("keys.txt", sep=';')
    Words = dfk['Words'].values
    df0 = df[(df.target == '0')]
    df1 = df[(df.target == '1')]

    # df.insert(3, 'target', " ", allow_duplicates=True)
    # df.to_csv(file, index=False, sep=',')

    stat = {}
    createDict(df)

    s = ""
    u = False

    while 1:

        n = random.randint(0, len(df) - 1)
        # --------------------------------- Error cases -------------------------------------
        if s != "" and s not in df.at[n, "text"]:  # ricerca per parola
            continue
        if (u is False) and (
                df.at[n, 'target'] == "0" or df.at[
            n, "target"] == "1"):  # non voglio modificare e sono già classificate
            continue
        if (u is True) and (  # voglio modificare e non sono classificate
                df.at[n, 'target'] != "0" and df.at[n, "target"] != "1"):
            continue

        createDict(df)

        print(".....................................................................................................")
        print("[", n, "]")
        print(df.at[n, 'text'])
        print(".....................................................................................................\n")

        if u is True:  # se già classificati (modalità update)
            print("\n***Actual label: ", df.at[n, 'target'], "***\n")

        print("\n---------------------------------------------------------------------------------------------------\n"
              "u : Modifica\ts: Parola da cercare\tstat: Statistiche\tspace: new "
              "iteration\t f = cerca id"
              "\n---------------------------------------------------------------------------------------------------\n")
        text = input(">> Label: ")

        if text != "0" and text != "1":

            if text == "stat":
                createDict(df)

            if text == "f":
                id = input(">> Insert id: ")
                id = int(id)
                print(df.at[id, 'text'])
                l = input(">> Insert value: ")
                df.at[id, 'target'] = l
                createDict(df)
                df.to_csv(file, index=False, sep=',')

            if text == "s":  # Select new word
                s = input(">> Insert word to find: ")

            if text == "u":  # update modes
                u = not u

        if text == "0" or text == "1" or text == "":
            # Set cell value at nth row and 4rt column
            df.at[n, 'target'] = text
            df.to_csv(file, index=False, sep=',')

            text = ""
