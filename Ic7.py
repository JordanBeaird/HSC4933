############################
#IC.7 # Jordan Beaird, 2026#
#--------------------------#
#Beaird@usf.edu            #
#--------------------------#
#Linear Regression         #
############################
# HSC 4933 - Week 7 Linear Regression
# Linear Regression of Pulse Rate and Systolic Blood Pressure

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

#  Load the dataset

df = pd.read_csv("Blood_Pressure_clean.csv")

print("dataset")
print(df.head())
print()

#  Check the data

print("Descriptive Statistics")
print(df.describe())
print()
print(df[["pulse_bpm", "sys_mmhg"]].describe())
print()

print("Missing Values")
print(df[["pulse_bpm", "sys_mmhg"]].isnull().sum())
print()


# Define the variables

# Independent variable (X): Pulse rate
# Dependent variable (Y): Systolic blood pressure

X = df["pulse_bpm"]
y = df["sys_mmhg"]

# Add the intercept to the model
X = sm.add_constant(X)

# Fit the linear regression model

model = sm.OLS(y, X).fit()

print("linear regression result")
print(model.summary())
print()

# Regression equation

intercept = model.params["const"]
slope = model.params["pulse_bpm"]
r_squared = model.rsquared
p_value = model.pvalues["pulse_bpm"]

print("Regression equation")
print(f"Predicted systolic blood pressure = "
      f"{intercept:.2f} + {slope:.3f}(pulse rate)")
print()

# Interpretation

print("Interpretation")
print()

print(
    f"For every 1 bpm increase in pulse rate, predicted "
    f"systolic blood pressure changes by approximately "
    f"{slope:.3f} mmHg."
)

print(
    f"The R-squared value is {r_squared:.4f}, meaning that "
    f"pulse rate explains approximately {r_squared * 100:.2f}% "
    f"of the variation in systolic blood pressure."
)

print(
    f"The p-value for pulse rate is {p_value:.4f}."
)

if p_value < 0.05:
    print(
        "Because the p-value is less than 0.05, pulse rate is "
        "a statistically significant predictor of systolic "
        "blood pressure."
    )
else:
    print(
        "Because the p-value is greater than 0.05, pulse rate "
        "is not a statistically significant predictor of "
        "systolic blood pressure."
    )

# Create scatterplot

plt.scatter(df["pulse_bpm"], df["sys_mmhg"])

plt.xlabel("Pulse Rate (bpm)")
plt.ylabel("Systolic Blood Pressure (mmHg)")
plt.title("Pulse Rate vs. Systolic Blood Pressure")

plt.savefig("pulse_vs_systolic_bp.png")
plt.show()

# Create residual plot

plt.scatter(model.fittedvalues, model.resid)

plt.axhline(y=0)

plt.xlabel("Fitted Values")
plt.ylabel("Residuals")
plt.title("Residual Plot")

plt.savefig("residual_plot.png")
plt.show()

