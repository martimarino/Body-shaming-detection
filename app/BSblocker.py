# This is a sample Python script.
from tkinter.messagebox import showerror

import ui
import tkinter as tk
from tkinter import ttk, END, LEFT, BOTH, CENTER, RIGHT, font


# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def error(error):
    showerror("Error", error)

def show_users(username, mylist):
    print(username)
    mylist.insert(END,username)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = tk.Tk()
    root.title('BSblocker')
    root.geometry('600x400+50+50')
    root.resizable(False, False)
    root.attributes('-topmost', 1)
    welcome = tk.Label(root, text='Welcome to BSblocker', font=('System Bold',20,'bold'), fg="white", bg="#1DA1F2", pady=10).pack()
    # root.iconbitmap('./assets/pythontutorial.ico')
    time = tk.Label(root, text='Select time period:', font=('System Bold',15,'bold'), fg="white", bg="#1DA1F2", pady=10).pack()
    selected_month = tk.StringVar()
    month_cb = ttk.Combobox(root, textvariable=selected_month)
    month_cb['values'] = ('1 min', '5 min', '10 min')
    month_cb['state'] = 'readonly'
    month_cb.set('Select interval to scrape')
    month_cb.pack(fill=tk.X, padx=150, pady=15)
    start_button = ttk.Button(
        root,
        text='Start',
        command=lambda: ui.start_scraping(selected_month.get(), mylist)
    )

    start_button.pack(
        ipadx=30,
        ipady=5
        #expand=True      //position centered
    )

    frame = tk.Frame(root)
    frame.pack(fill="both", padx=150, pady=30)
    scrollbar = ttk.Scrollbar(frame, orient='vertical')
    scrollbar.pack(side=RIGHT,fill="y")
    mylist = tk.Listbox(frame, yscrollcommand=scrollbar.set)
    #mylist.pack(expand=1, fill="both")
    mylist.pack(fill="both")

    scrollbar.config(command=mylist.yview)

    #******************* STYLE *****************
    root.configure(background='#1DA1F2')


    root.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
