import pandas as pd
import re

input_file = '../raw_scraped/2022-06.csv'
output_file = '../cleaned/2022-06-cleaned.csv'

# remove dup
df = pd.read_csv(input_file, index_col=False, delimiter=",")
df.drop_duplicates(subset=['text', 'username'])

dfk = pd.read_csv("../keys.txt", sep=';')
Words = dfk['Words'].values

tweets_list = []
how_many = 0
found = 0


# insert 'target' column
df.insert(3, 'target', " ", allow_duplicates=True)
df.to_csv(output_file, index=False, sep=',')

for i in range(len(df)):

    # remove URLs and mentions
    df.at[i, 'text'] = re.sub(r"(?:\@|https?\://)\S+", '', df.at[i, 'text'], flags=re.MULTILINE)

    # remove new lines
    if df.at[i, 'text'].endswith("\n") or df.at[i, 'text'].endswith("\r"):
        df.at[i, 'text'] = df.at[i, 'text'].replace("\n", "").replace("\r", "")
    else:
        df.at[i, 'text'] = df.at[i, 'text'].replace("\n", " ").replace("\r", " ")

    # remove multiple spaces
    df.at[i, 'text'] = re.sub('\\s+', ' ', df.at[i, 'text'])

    # remove tweets without keywords
    for word in Words:

        found = 0

        if word in df.at[i, 'text'].lower():

            found = 1

            tweets_list.append(
                [df.at[i, 'datetime'], df.at[i, 'text'], df.at[i, 'username'], df.at[i, 'target']])

            how_many = how_many + 1

            if i % 100 == 0:
                print("Tweets filtered: ", how_many, "\t\tdate: ", df.at[i, 'datetime'])

            break
    if found == 0:
        print("Deleted: ", df.at[i, 'text'])

tweets_df = pd.DataFrame(tweets_list, columns=['datetime', 'text', 'username', 'target'])
tweets_df.to_csv(output_file, index=False, sep=',')
print(tweets_df.shape)
