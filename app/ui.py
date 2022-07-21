from tkinter import END

import BSblocker
import scrape
from datetime import datetime, timedelta
last_time = datetime.now() + timedelta(minutes=5)
print(last_time.strftime('%Y-%m-%d %H:%M:%S'))


def start_scraping(minutes, mylist, started):
    if(minutes == "Select interval to scrape"):
        BSblocker.error("Minutes not specified")
        return
    else:
        mylist.delete(0,END)
        minutes = minutes.split()
        print(minutes[0])
        scrape.getFilteredTweets(minutes[0], mylist, started)


# def main():
#     pass
#
# if __name__ == "__main__":
#     main()