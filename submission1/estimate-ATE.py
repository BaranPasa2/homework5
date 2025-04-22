import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import seaborn as sns
from scipy.stats import pearsonr
import numpy as np
import pyfixest as pf


insurance = pd.read_csv('data/output/acs_insurance.txt', sep="\t")
medicaid = pd.read_csv("data/output/acs_medicaid.txt", sep="\t")
medicaid_expansion = pd.read_csv("data/output/medicaid_expansion.txt", sep="\t")

#Point 5:
avg_2012 = insurance[insurance['year'] == 2012]
avg_2015 = insurance[insurance['year'] == 2015]



avg_2012["yearly_total"] = (
    avg_2012["ins_employer"] +
    avg_2012["ins_direct"] +
    avg_2012["ins_medicare"] +
    avg_2012["ins_medicaid"] +
    avg_2012["uninsured"]
)

avg_2015["yearly_total"] = (
    avg_2015["ins_employer"] +
    avg_2015["ins_direct"] +
    avg_2015["ins_medicare"] +
    avg_2015["ins_medicaid"] +
    avg_2015["uninsured"]
)
