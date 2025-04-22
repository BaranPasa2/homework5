import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import seaborn as sns
from scipy.stats import pearsonr
import numpy as np

insurance = pd.read_csv('data/output/acs_insurance.txt', sep="\t")
medicaid = pd.read_csv("data/output/acs_medicaid.txt", sep="\t")
medicaid_expansion = pd.read_csv("data/output/medicaid_expansion.txt", sep="\t")

# Point 1:

insur_per_year = insurance.copy()
insur_per_year = insur_per_year.groupby('year', as_index=False)['ins_direct'].sum()

insur_totals = insurance.copy()
insur_totals = insur_totals.groupby("year", as_index=False)[
    ["ins_employer", "ins_direct", "ins_medicare", "ins_medicaid", "uninsured"]
].sum()

# Calculate the yearly total population
insur_totals["yearly_total"] = (
    insur_totals["ins_employer"] +
    insur_totals["ins_direct"] +
    insur_totals["ins_medicare"] +
    insur_totals["ins_medicaid"] +
    insur_totals["uninsured"]
)
insur_per_year = pd.merge(
    insur_per_year,
    insur_totals[['year', 'yearly_total']],
    on="year",
    how='left'
    )

insur_per_year['ins_direct_percent'] = insur_per_year['ins_direct'] / insur_per_year['yearly_total']
print(insur_per_year.head())

plt.figure(figsize=(10, 6))
plt.plot(insur_per_year["year"], insur_per_year["ins_direct_percent"], marker='o', linewidth=2)

plt.title("Total Direct Insurance Coverage by Year")
plt.xlabel("Year")
plt.ylabel("Percent of US Adult Population with Direct Insurance")
plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1))  # use 100 if your values are 0–100
plt.grid(True)
plt.tight_layout()
plt.show()

# Point 3:
medicaid_per_year = medicaid.groupby('year', as_index=False)['ins_medicaid'].sum()
medicaid_per_year = pd.merge(
    medicaid_per_year,
    insur_totals[['year', 'yearly_total']],
    on="year",
    how='left'
    )

medicaid_per_year['medicaid_percent'] = medicaid_per_year['ins_medicaid'] / medicaid_per_year['yearly_total']

plt.figure(figsize=(10, 6))
plt.plot(medicaid_per_year["year"], medicaid_per_year["medicaid_percent"], marker='o', linewidth=2)

plt.title("Medicaid Insurance Coverage by Year")
plt.xlabel("Year")
plt.ylabel("Percent of US Adult Population with Medicaid")
plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1))  # use 100 if your values are 0–100
plt.grid(True)
plt.tight_layout()
plt.show()

# Point 4
df_ins = insurance
df_exp = medicaid_expansion

# Clean and prepare expansion data
df_exp["expand_year"] = pd.to_datetime(df_exp["date_adopted"], errors="coerce").dt.year
df_exp = df_exp[["State", "expand_year"]]

# Merge with insurance data
df_merged = pd.merge(df_ins, df_exp, on="State", how="left")
# Label whether a state was expanded that year or not
df_merged["expanded"] = df_merged.apply(
    lambda row: "Expansion" if pd.notna(row["expand_year"]) and row["year"] >= row["expand_year"]
    else "Non-Expansion",
    axis=1
)


# Group by year and expansion status, summing ins_direct
df_grouped = df_merged.groupby(["year", "expanded"])["uninsured"].sum().reset_index()
df_grouped = pd.merge(df_grouped, insur_totals[['year', 'yearly_total']], on="year", how='left')
df_grouped['uninsured_expand_per'] = df_grouped['uninsured'] / df_grouped['yearly_total']

# Pivot to get columns for plotting
df_pivot = df_grouped.pivot(index="year", columns="expanded", values="uninsured_expand_per")

# Plotting
plt.figure(figsize=(10, 6))
df_pivot.plot(marker='o', linewidth=2)
plt.title("Uninsured Population Relative to Medicaid Expansion")
plt.ylabel("Total Uninsured")
plt.xlabel("Year")
plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1))  # use 100 if your values are 0–100
plt.grid(True)
plt.tight_layout()
plt.legend(title="Medicaid Expansion Status")
plt.show()