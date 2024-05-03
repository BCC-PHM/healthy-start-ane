# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename
import ctypes  # An included library with Python install.   
import sys

tk.Tk().withdraw()
file_name = askopenfilename()

try:
    # Try to open the excel file
    xl = pd.ExcelFile(file_name)
except Exception:
    # If it fails to open, give error message
    ctypes.windll.user32.MessageBoxW(0, "Couldn't open Excel file. This is probably because the file is already open.", "Error!", 1)
    sys.exit()
    
    
# Load all sheets
df_list = [xl.parse(sheet_i) for sheet_i in xl.sheet_names]

# Combine all sheets and remove empty rows
df = pd.concat(df_list).dropna(subset = ["Vitamins Provided"])

# Convert age to number of years
df["Age (Years)"] = df["Age"].str.extract(r'^([\d]+) year').fillna("0")
df["Age (Years)"] = pd.to_numeric(df["Age (Years)"])

### Standardise vitamin numbers ###

# Vitamins provided for current child
df["Vitamins Provided"] = np.where(
    df["Vitamins Provided"] == "Yes", 1, 0
    )

# Vitamins provided for siblings
df["Number of Silbings \nprovided with Vitamins"] = df["Number of Silbings \nprovided with Vitamins"].fillna(0)

# Vitamins provided for mother
df[" Vitamins provide for Mum "] = np.where(
    df[" Vitamins provide for Mum "] == "Yes", 1, 0
    )

# Total vitamins
df["Total vitamins provided"] = df["Vitamins Provided"] + \
    df["Number of Silbings \nprovided with Vitamins"] + \
    df[" Vitamins provide for Mum "]

print(df)

# file_name = "../data/Healthy Start Vitamins.xlsx"