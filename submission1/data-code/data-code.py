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
print(insurance.head())
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


# Plotting
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
medicaid_per_year = insurance.groupby('year', as_index=False)['ins_medicaid'].sum()
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