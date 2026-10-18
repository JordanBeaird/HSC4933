
################################################
# Lab 7: Linear Regression #
#---------------------------------------------#
# Odelia Asher # oasher@usf.edu # 10/11/2026
# Improvements by: Jordan Beaird
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
    print("1. Birthwt.csv")
    print("2. Places_2025.csv")

    dataset_choice = input("Please select the dataset you would like to use:")
    return dataset_choice

# This variable stores the user's selection
dataset_choice = chosen_dataset()

# If a user selects option 1, load the Birthwt.csv dataset
if dataset_choice == "1":
    CSV_PATH = "../birthwt.csv"
    df = pd.read_csv(CSV_PATH)

# If a user selects option 2, load the Places_2025.csv dataset
elif dataset_choice == "2":
    CSV_PATH = "../places_2025.csv"
    df = pd.read_csv(CSV_PATH)

else:
    print("Dataset not available")
    exit()

# Clean the column names of the chosen dataset to snake case format
df.columns = df.columns.str.lower().str.replace(' ', '_')

"""
List available column names of the chosen dataset and prompt user for the column
name they want as the X variable and the Y variable
"""

def column_name():
    print("Dataset column names:")

    columns = list(df.columns)
    midpoint = (len(columns)+1)//2

    for i in range(midpoint):
        left = columns[i]
        right = columns[i+midpoint] if i + midpoint < len(columns) else ""
        print(f"{left:<30}{right}")

    X_COL = input("Please enter the column name you would like to use for the X variable:")
    Y_COL = input("Please enter the column name you would like to use for the Y variable:")

    if X_COL not in df.columns or Y_COL not in df.columns:
        print("Invalid column name. Please choose an available column")
        return None

    return X_COL, Y_COL

# This variable stores the user's selection
selected_columns = column_name()

if selected_columns is None:
    exit()

X_COL, Y_COL = selected_columns

# Select chosen columns
data = df[[X_COL, Y_COL]].copy()

# Remove commas and convert values to numbers
for col in [X_COL, Y_COL]:
    data[col] = pd.to_numeric(data[col].astype(str).str.replace(",", "", regex=False), errors="coerce")

# Remove rows missing either of the values used for regression
data = data.dropna()


# IMPROVEMENT 1: Allow regression for specific ranges of data
filter_choice = input("Would you like to filter the X variable by a specific range? (yes/no):")

if filter_choice == "yes":
    min_value = float(input("Enter the minimum X value:"))
    max_value = float(input("Enter the maximum X value:"))

    data = data[(data[X_COL] >= min_value) & (data[X_COL] <= max_value)]

    print(f"Number of observations in selected range: {len(data)}")

# Check that enough data remains for regression
if len(data) < 3 or data[X_COL].nunique() < 2:
    print("Not enough data for regression.")
    exit()


# IMPROVEMENT 2: Allow users to customize plot formatting
scatter_color = input("Enter scatterplot color (press Enter for blue):")
if scatter_color == "":
    scatter_color = "blue"

line_color = input("Enter regression line color (press Enter for crimson):")
if line_color == "":
    line_color = "crimson"

line_width = input("Enter regression line thickness (press Enter for 2):")
if line_width == "":
    line_width = 2
else:
    line_width = float(line_width)

custom_title = input("Enter a custom graph title (press Enter for default):")

grid_choice = input("Would you like gridlines? (yes/no):")


# Create a scatterplot of the values without a regression line
fig, ax = plt.subplots(figsize=(8,6))
ax.scatter(data[X_COL], data[Y_COL], color=scatter_color, alpha=0.6, edgecolors="k", linewidth=0.3)
ax.set_xlabel(X_COL)
ax.set_ylabel(Y_COL)

if custom_title == "":
    ax.set_title(f"{Y_COL} vs. {X_COL} (n={len(data)})")
else:
    ax.set_title(custom_title)

if grid_choice == "yes":
    ax.grid(alpha=0.3)

fig.tight_layout()

"""
Ask user if they would like to save the scatter plot file and save the scatterplot with a
custom file name
"""

def save_scatterplot():
    print("Would you like to save the scatter plot?")

    scatterplot_choice = input("Please enter yes or no:")

    if scatterplot_choice == "yes":
        scatter_file_name = input("Please enter the file name you would like to save the scatter plot:")
        scatter_file = f"{scatter_file_name}.png"
        fig.savefig(scatter_file, dpi=300)
        print(f"Saved scatterplot -> {scatter_file}")

    elif scatterplot_choice == "no":
        print("Scatterplot not saved ")

save_scatterplot()

# Calculate the OLS regression line
X = sm.add_constant(data[X_COL])
model = sm.OLS(data[Y_COL], X).fit()

# Print regression summary
print("OLS Regression Summary:")
print(model.summary())

# Plot the OLS regression line on the scatterplot
x_line = np.linspace(data[X_COL].min(), data[X_COL].max(), 100)
y_line = model.params.iloc[0] + model.params.iloc[1] * x_line
ax.plot(x_line, y_line, color=line_color, linewidth=line_width, label=f"OLS Line (R²= {model.rsquared:.3f})")

if custom_title == "":
    ax.set_title(f"{Y_COL} vs. {X_COL} with OLS line (n={len(data)})")
else:
    ax.set_title(custom_title)

ax.legend()

"""
Ask user if they would like to save the scatterplot with the OLS regression line and save the file
with a custom file name
"""

def save_ols_scatterplot():
    print("Would you like to save the scatter plot with the OLS regression line:")
    OLS_choice = input("Please enter yes or no:")

    if OLS_choice == "yes":
        OLS_file_name = input("Please enter the file name you would like to save the file with:")
        OLS_file = f"{OLS_file_name}.png"
        fig.savefig(OLS_file, dpi=300)
        print(f"Saved OLS plot with OLS Regression line-> {OLS_file}")

    elif OLS_choice == "no":
        print("Scatterplot with OLS Regression line not saved ")

save_ols_scatterplot()
plt.show()

