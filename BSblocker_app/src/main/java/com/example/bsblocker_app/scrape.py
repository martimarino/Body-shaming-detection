import pandas as pd
from tweepy import Stream
import pandas as pd

from datetime import datetime, timedelta
last_time = datetime.now() + timedelta(minutes=5)
print(last_time.strftime('%Y-%m-%d %H:%M:%S'))

df = pd.DataFrame([["1", "2", "3"]], columns=["1", "2", "3"])
print(df)

df.to_csv("scrape_prova.csv", index=False)