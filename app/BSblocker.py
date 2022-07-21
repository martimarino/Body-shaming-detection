# This is a sample Python script.

import csv
import os
from tkinter.messagebox import showerror

import pandas as pd

import ui
import tkinter as tk
from tkinter import ttk, END, LEFT, BOTH, CENTER, RIGHT, font

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def error(error):
    showerror("Error", error)

def show_users(username, mylist, start_button):
    print(username)
    mylist.insert(END,username)

    with open("./users_found.csv", 'r', newline='', encoding="utf8") as f:
        counter = 0
        reader = csv.reader(f)
        headings = next(reader)
        for row in reader:
            if row[2] == username:
                counter += 1
    df = pd.DataFrame([[username]], columns=['Username'])

    started = False
    if not os.path.isfile("./blacklist.csv"):
        df.to_csv("./blacklist.csv", header='column_names', index=False)
    if counter >= 5:
        mylist.itemconfig(END, {'bg': 'red'})
        with open("./blacklist.csv", 'r', newline='', encoding="utf8") as f:
            reader = csv.reader(f)
            headings = next(reader)
            for row in reader:
                if row[0] == username:
                    return

        if not os.path.isfile("./blacklist.csv"):
            df.to_csv("./blacklist.csv", header='column_names', index=False)
        else:  # else it exists so append without writing the header
            df.to_csv("./blacklist.csv", mode='a', header=False, index=False)

# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    root = tk.Tk()
    root.title('BSblocker')
    root.iconbitmap('BSblocker_free-file.ico')
    root.geometry('650x450+100+100')
    root.resizable(False, False)
    root.attributes('-topmost', 1)
    started = False
    #welcome = tk.Label(root, text='Welcome to BSblocker', font=('System Bold',20,'bold'), fg="white", bg="#1DA1F2", pady=10).pack()
    img = tk.PhotoImage(file="BSblocker_free-file.png")
    tk.Label(root, image=img, bg='#1DA1F2').pack()
    # root.iconbitmap('./assets/pythontutorial.ico')
    time = tk.Label(root, text='Select time period:', font=('System Bold',15,'bold'), fg="white", bg="#1DA1F2", pady=10).pack()
    selected_month = tk.StringVar()
    month_cb = ttk.Combobox(root, textvariable=selected_month)
    month_cb['values'] = ('1 min', '5 min', '10 min')
    month_cb['state'] = 'readonly'
    month_cb.set('Select interval to scrape')
    month_cb.pack(fill=tk.X, padx=150, pady=15)
    buttonFont = font.Font(family='System Bold', size=13)
    start_button = tk.Button(
        root,
        text='Start',
        command=lambda: ui.start_scraping(selected_month.get(), mylist, started),
        font=buttonFont,
        bg='#E1E8ED',
        borderwidth=0
    )
    start_button['state'] = 'normal'
    start_button.pack(
        ipadx=30,
        ipady=3
        #expand=True      //position centered
    )
    frame = tk.Frame(root)
    frame.pack(fill="both", padx=150, pady=30)

    scrollbar = ttk.Scrollbar(frame, orient='vertical')
    scrollbar.pack(side=RIGHT,fill="y")
    mylist = tk.Listbox(frame, yscrollcommand=scrollbar.set)
    mylist.pack(fill="both")

    scrollbar.config(command=mylist.yview)

    #******************* STYLE *****************
    root.configure(background='#1DA1F2')


    root.mainloop()