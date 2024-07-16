# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import ctypes
import sys
import easygui


file_name = easygui.fileopenbox()

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
df["Age (Years)"] = pd.to_numeric(df["Age (Years)"], downcast='integer')


### Clean up Yes/No columns ###
for col_i in ["Vitamins Provided", " Vitamins provide for Mum "]:
    # Replace NA with "No"
    df[col_i] = df[col_i].fillna("No")
    # Replace 0 with "No"
    df.loc[df[col_i] == 0, col_i] = "No"
    # Replace 1 with "Yes"
    df.loc[df[col_i] == 1, col_i] = "Yes"
    # Standardise spaces and capitalisation
    df[col_i] = [item.strip().title() for item in df[col_i]]
    # Check that column is just "Yes" or "No"
    assert all(df[col_i].isin(["Yes", "No"])), \
        "Error: {} column consaints unexpected values".format(col_i)
    # Convert to 1 and 0
    df[col_i] = np.where(
        df[col_i] == "Yes", 1, 0
        )

# Vitamins provided for siblings
df["Number of Silbings \nprovided with Vitamins"] = df["Number of Silbings \nprovided with Vitamins"].fillna(0.0)
sibling_string_mask = df["Number of Silbings \nprovided with Vitamins"].apply(lambda x: isinstance(x, str))
# S
df.loc[sibling_string_mask, "Number of Silbings \nprovided with Vitamins"] = \
    [item.strip().lower() for item in df.loc[sibling_string_mask, 
                                             "Number of Silbings \nprovided with Vitamins"]]
df.loc[df["Number of Silbings \nprovided with Vitamins"].isin(["na", "n/a"]), "Number of Silbings \nprovided with Vitamins"] = 0


# Total vitamins
df["Total vitamins provided"] = df["Vitamins Provided"] + \
    df["Number of Silbings \nprovided with Vitamins"] + \
    df[" Vitamins provide for Mum "]

### Fill Unknown Ethnicities ###
df['Ethnicity'] = df['Ethnicity'].fillna("Unknown")

### Join IMDs ###
imds = pd.read_csv("../data/birmingham-imds.csv", 
                   dtype = {'Postcode': str, 
                            'IMD Quintile 2019': str})

df = df.merge(imds, on='Postcode', how = "left")
df['IMD Quintile 2019'] = df['IMD Quintile 2019'].fillna("Unknown")
# Check if it's a Birmingham Postcode
df["Birmingham Postcode"] = np.where(
    df['IMD Quintile 2019'] != "Unknown", "Yes", 
    np.where(df['Postcode'].isnull(), "Unknown", "No"))

### Count by ###

# ethnicity
df_eth = df.groupby("Ethnicity")["Total vitamins provided"].sum().reset_index()

# IMD
df_imd = df.groupby("IMD Quintile 2019")["Total vitamins provided"].sum().reset_index()

# In Birmingham
df_brum = df.groupby("Birmingham Postcode")["Total vitamins provided"].sum().reset_index()

### Save data ###

# Request save name
save_name = easygui.enterbox("Enter name for the new file. (Please don't include / or \\)")

# Remove common file extensions
for suffix in [".csv",".xls", ".xlsx"]:
    save_name = save_name.replace(suffix, "")

# Make full save path based on original file
save_prefix = "\\".join(file_name.split("\\")[:-1])
save_path = save_prefix + "\\" + save_name + ".xlsx"

with pd.ExcelWriter(save_path) as writer:
   
    # use to_excel function and specify the sheet_name and index 
    # to store the dataframe in specified sheet
    df.to_excel(writer, sheet_name="Data", index=False)
    df_eth.to_excel(writer, sheet_name="Ethnicity", index=False)
    df_imd.to_excel(writer, sheet_name="IMD", index=False)
    df_brum.to_excel(writer, sheet_name="In Birmingham", index=False)
    
print("Done.")