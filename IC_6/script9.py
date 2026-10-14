################################################
# Lab 7: Linear Regression #
#---------------------------------------------#
# Odelia Asher # oasher@usf.edu # 10/11/2026
###############################################

"""
This script allows users to select a dataset and choose
X and Y variables to create a scatter plot, calculate
and display an OLS regression line.
"""

# Import libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Prompt user for a specific dataset
def chosen_dataset():
    print ("1. Birthwt.csv")
    print ("2. Places_2025.csv")

    dataset_choice = input ("Please select the dataset you would like to use:")
    return dataset_choice

# This variable stores the user's selection
dataset_choice = chosen_dataset()

# If a user selects option 1, load the Birthwt.csv dataset
if dataset_choice == "1":
    CSV_PATH = "birthwt (1).csv"
    df = pd.read_csv(CSV_PATH)

# If a user selects option 2, load the Places_2025.csv dataset
elif dataset_choice == "2":
    CSV_PATH = "places_2025 (2).csv"
    df = pd.read_csv(CSV_PATH)

else:
    print ("Dataset not available")
    exit()

# Clean the column names of the chosen dataset to snake case format
df.columns = df.columns.str.lower().str.replace(' ', '_')

""" 
List available column names of the chosen dataset and prompt user for the column
name they want as the X variable and the Y variable
"""

def column_name():
    print ("Dataset column names:")

    columns = list (df.columns)
    midpoint = (len(columns)+1)//2

    for i in range(midpoint):
        left = columns[i]
        right = columns[i+midpoint] if i + midpoint < len(columns) else""
        print (f"{left:<30}{right}")

    X_COL = input ("Please enter the column name you would like to use for the X variable:")
    Y_COL = input ("Please enter the column name you would like to use for the Y variable:")

    if X_COL not in df.columns or Y_COL not in df.columns:
        print ("Invalid column name. Please choose an available column")
        return None

    return X_COL, Y_COL

# This variable stores the user's selection
X_COL, Y_COL = column_name()

# Select chosen columns
data = df[[X_COL, Y_COL]].copy()

# Remove commas and convert values to numbers
for col in [X_COL, Y_COL]:
    data[col] = pd.to_numeric(data[col].astype(str).str.replace(",","",regex= False), errors="coerce")

# Remove rows missing either of the values used for regression
data = data.dropna()

# Create a scatterplot of the values without a regression line
fig,ax = plt.subplots(figsize=(8,6))
ax.scatter(data[X_COL],data[Y_COL],alpha=0.6, edgecolors="k", linewidth=0.3)
ax.set_xlabel(X_COL)
ax.set_ylabel(Y_COL)
ax.set_title(f"{Y_COL} vs. {X_COL} (n={len(data)})")
ax.grid(alpha=0.3)
fig.tight_layout()

"""
Ask user if they would like to save the scatter plot file and save the scatterplot with a 
custom file name 
"""

def save_scatterplot():
    print ("Would you like to save the scatter plot?")

    scatterplot_choice = input ("Please enter yes or no:")

    if scatterplot_choice == "yes":
        scatter_file_name = input ("Please enter the file name you would like to save the scatter plot:")
        scatter_file = f"{scatter_file_name}.png"
        fig.savefig(scatter_file,dpi=300)
        print (f"Saved scatterplot -> {scatter_file}")

    elif scatterplot_choice == "no":
        print (f"Scatterplot not saved ")

save_scatterplot()

# Calculate the OLS regression line
X = sm.add_constant(data[X_COL])
model = sm.OLS(data[Y_COL], X).fit()

# Print regression summary
print ("OLS Regression Summary:")
print (model.summary())

# Plot the OLS regression line on the scatterplot
x_line = np.linspace(data[X_COL].min(), data[X_COL].max(), 100)
y_line = model.params ["const"] + model.params [X_COL] * x_line
ax.plot(x_line,y_line,color="crimson", linewidth = 2, label = f"OLS Line (R²= {model.rsquared:.3f})")
ax.set_title(f"{Y_COL} vs. {X_COL} with OLS line (n={len(data)})")
ax.legend()

"""
Ask user if they would like to save the scatterplot with the OLS regression line and save the file
with a custom file name"""

def save_ols_scatterplot():
    print ("Would you like to save the scatter plot with the OLS regression line:")
    OLS_choice = input ("Please enter yes or no:")

    if OLS_choice == "yes":
        OLS_file_name = input ("Please enter the file name you would like to save the file with:")
        OLS_file = f"{OLS_file_name}.png"
        fig.savefig(OLS_file,dpi=300)
        print (f"Saved OLS plot with OLS Regression line-> {OLS_file}")

    elif OLS_choice == "no":
        print (f"Scatterplot with OLS Regression line not saved ")

save_ols_scatterplot()
plt.show()
