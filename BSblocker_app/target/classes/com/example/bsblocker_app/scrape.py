
import twint
import pandas as pd

c = twint.Config()

c.Search = ['Taylor Swift']       # topic
c.Limit = 500      # number of Tweets to scrape
c.Store_csv = True       # store tweets in a csv file
c.Output = "body_shaming_tweets.csv"     # path to csv file

twint.run.Search(c)
df = pd.read_csv('body_shaming_tweets.csv')

