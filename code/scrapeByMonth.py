import snscrape.modules.twitter as sntwitter
import pandas as pd

def getFilteredTweets():
    text_query = '("grasso" OR "grassa" ' \
                 'OR "ciccione"' \
                 'OR "culone" OR "nano" ' \
                 'OR "nana" OR "obeso" ' \
                 'OR "pelata" OR "pelato")'
    since_date = '2022-06-01'
    until_date = '2022-07-01'
    options = '-is:retweet -is:reply -is:quoted lang:it'
    output_file = '../raw_scraped/2022-06.csv'
    tweets_list = []
    fetched = 0

    print("output_file: ", output_file)

    for i, tweet in enumerate(
            sntwitter.TwitterSearchScraper(
                text_query + ' since:' + since_date + ' until:' + until_date + ' ' + options).get_items()):
        dfk = pd.read_csv("../keys.txt", sep=';')

        Words = dfk['Words'].values
        print(Words)
        for word in Words:
            if word in tweet.content:

                fetched = fetched+1

                tweets_list.append(
                    [tweet.date, tweet.content, tweet.user.username])

                if i % 100 == 0:
                    print("Tweets obtained: ", fetched, "\t\tdate: ", tweet.date)

                break

    tweets_df = pd.DataFrame(tweets_list,
                             columns=['datetime', 'text', 'username'])
    tweets_df.to_csv(output_file, index=False, sep=',')


if __name__ == '__main__':
    getFilteredTweets()