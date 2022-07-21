import os
from datetime import datetime, timedelta
import pytz

utc = pytz.UTC

import snscrape.modules.twitter as sntwitter
import pandas as pd
import preprocessing

def getFilteredTweets(interval, mylist, started):
    # today = datetime.now() - timedelta(minutes=int(interval))
    start_time = datetime.now() - timedelta(days=1)  # date start scraping    20-07-2022 - 1 giorno = 19-07-2022
    end_time = start_time + timedelta(days=1)  # date end scraping   19-07-2022 + 1 giorno = 20-07-2022
    now = datetime.now()
    start = now - timedelta(hours=2) - timedelta(
        minutes=int(interval))  # date now   16:22 - 2 ore = 14:22 - 5min = 14:17
    end = start + timedelta(minutes=int(interval))  # time end date  14:17 + 5min = 14:22
    start_time = start_time.strftime('%Y-%m-%d')
    end_time = end_time.strftime('%Y-%m-%d')
    print(start_time, end_time)

    text_query = '("grasso" OR "grassa" ' \
                 'OR "ciccione" ' \
                 'OR "culone" OR "nano" ' \
                 'OR "nana" OR "obeso" ' \
                 'OR "pelata" OR "pelato")'
    since_date = start_time
    options = '-is:retweet -is:reply -is:quoted lang:it'
    output_file = './scraped/' + start.strftime("%Y-%m-%d_%H-%M-%S") + '.csv'
    tweets_list = []
    fetched = 0

    dfk = pd.read_csv("keys.txt", sep=';')
    print("output_file: ", output_file)

    for i, tweet in enumerate(
            sntwitter.TwitterSearchScraper(
                text_query + ' since:' + since_date + ' ' + options).get_items()):

        Words = dfk['Words'].values
        for word in Words:
            if word in tweet.content:
                print(tweet.date)
                if start.replace(tzinfo=utc) < tweet.date < end.replace(tzinfo=utc):
                    fetched = fetched + 1
                    print(tweet.content)
                    text = preprocessing.clean(tweet.content)
                    if text == "":
                        break
                    preprocessing.prep(tweet.date, tweet.user.username, text, start.strftime("%Y-%m-%d_%H-%M-%S")+".csv", mylist, started)
                    tweets_list.append(
                        [tweet.date, tweet.content, tweet.user.username])

                    print("Tweets obtained: ", fetched, "\t\tdate: ", tweet.date)
                else:
                    tweets_df = pd.DataFrame(tweets_list,
                                             columns=['datetime', 'text', 'username'])

                    tweets_df.to_csv(output_file, index=False)
                    return

def main():
    pass


if __name__ == "__main__":
    main()
