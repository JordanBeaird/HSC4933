# Imports
import pandas as pd
import numpy as np

df = pd.read_csv("eye_health.csv")

#print csv stats before cleaning
print(df.shape,
      df.dtypes,
      df.isna().sum(),
      df.isnull().sum(),
      df.nunique()
      sep="/n")
#print number of duplicated values
print("Duplicates: ", df.duplicaed().sum())

df = df.dropna(axis=1, how="all")#Drop columns with no data
df= df.drop(column = [c for c in df.columns if c.endswith("ID")])   #Dop columns that end in ID

df= df.dropna(subset=["Data_Value"])# Drop rows with no value in the column "Data_Value"
df= dr.drop(columns=["Geolocation, "Data_Value_Footnote_Symbol", "Data_Value_Footnote" , "StateAbbr", "NonWeightedSample" , "Geographic Level", "Numerator""])

df.columns = df.columns.str.lower().str.replace(" ", "_")
df["error"] = (df["high_confidence_limit"] - df["low_confidence_limit"]) / 2
df["prevalence_level"] = np.select (condlist: var = [df["data_value"] < 5, df["data_value"] <= 7] choicelist: ["Low", "Medium"], default: "High")

df.to_csv(path_or_buf: "eye_health_2022_clean.csv", index=False)
print(pd.read_csv("eye_health_2022_clean.csv"). shape == df.shape)
print(pd.read_csv("eye_health_2022_clean.csv"). shape)
print(pd.read_csv("eye_health_2022_clean.csv"). head)



