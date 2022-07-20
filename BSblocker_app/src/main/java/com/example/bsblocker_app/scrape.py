import pandas as pd
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
last_time = datetime.now() + timedelta(minutes=5)
print(last_time.strftime('%Y-%m-%d %H:%M:%S'))

