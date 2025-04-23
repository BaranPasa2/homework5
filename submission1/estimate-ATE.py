import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import seaborn as sns
from scipy.stats import pearsonr
import numpy as np
import statsmodels.formula.api as smf


insurance = pd.read_csv('data/output/acs_insurance.txt', sep="\t")
medicaid = pd.read_csv("data/output/acs_medicaid.txt", sep="\t")
medicaid_expansion = pd.read_csv("data/output/medicaid_expansion.txt", sep="\t")

#Point 5:

# Load insurance and Medicaid expansion data
df_ins = insurance
df_expand = medicaid_expansion

# Convert expansion year from date
df_expand["expand_year"] = pd.to_datetime(df_expand["date_adopted"], errors="coerce").dt.year

# Merge datasets
df = pd.merge(df_ins, df_expand[["State", "expand_year"]], on="State", how="left")

# Label expansion status by 2015
df["expanded"] = df["expand_year"].apply(lambda x: "Expansion" if pd.notna(x) and x <= 2015 else "Non-Expansion")

# Filter to years 2012 and 2015
df_filtered = df[df["year"].isin([2012, 2015])].copy()
df_filtered["uninsured_rate"] = df_filtered["uninsured"] / df_filtered["adult_pop"]
dd_table = df_filtered.groupby(["year", "expanded"])["uninsured_rate"].mean().unstack()

dd_table = dd_table * 100
dd_table = dd_table.round(2)
dd_table.index = ["2012", "2015"]
print(dd_table)

# Point 6:

# Load the datasets
insurance_df = pd.read_csv("data/output/acs_insurance.txt", sep="\t")
medicaid_df = pd.read_csv("data/output/acs_medicaid.txt", sep="\t")

# Merge data
df = pd.merge(insurance_df, medicaid_df[['State', 'year', 'expand', 'expand_year']], 
              on=['State', 'year'], how='left')

# Filter to only 2014 expanders and never-expanders
df['treat_group'] = df['expand_year'] == 2014
df['control_group'] = df['expand'] == False
df = df[df['treat_group'] | df['control_group']]

# Treatment indicator
df['treated'] = df['treat_group'].astype(int)
df['post'] = (df['year'] >= 2014).astype(int)
df['did'] = df['treated'] * df['post']
df['uninsured_rate'] = df['uninsured'] / df['adult_pop']

# Run DiD regression with fixed effects for state and year
model = smf.ols(
    formula='uninsured_rate ~ treated + post + did + C(State) + C(year)',
    data=df
).fit(cov_type='cluster', cov_kwds={'groups': df['State']})

model.summary()
print(model.summary())