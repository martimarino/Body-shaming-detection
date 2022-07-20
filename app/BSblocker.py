# This is a sample Python script.
from tkinter.messagebox import showerror

import ui
import tkinter as tk
from tkinter import ttk, END, LEFT, BOTH, CENTER


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
    tk.Label(root, text='Welcome to BSblocker').pack()
    # root.iconbitmap('./assets/pythontutorial.ico')
    tk.Label(root, text='Select time period:').pack()
    selected_month = tk.StringVar()
    month_cb = ttk.Combobox(root, textvariable=selected_month)
    month_cb['values'] = ('1 min', '5 min', '10 min')
    month_cb['state'] = 'readonly'
    month_cb.pack(fill=tk.X, padx=5, pady=5)
    start_button = ttk.Button(
        root,
        text='Start',
        command=lambda: ui.start_scraping(selected_month.get(), mylist)
    )

    start_button.pack(
        ipadx=5,
        ipady=5
        #expand=True      //position centered
    )

    scrollbar = ttk.Scrollbar(root, orient='vertical')
    scrollbar.pack(fill=tk.X, padx=5, pady=5)
    mylist = tk.Listbox(root, yscrollcommand=scrollbar.set)
    mylist.pack(fill=BOTH)
    scrollbar.config(command=mylist.yview)
    root.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
