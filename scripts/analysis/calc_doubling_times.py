# ---
# jupyter:
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

from math import log
import pandas as pd
import numpy as np

# Add description here
#
# *Note:* You can open this file as a notebook (JupyterLab: right-click on it in the side bar -> Open With -> Notebook)


# +
# Uncomment the next two lines to enable auto reloading for imported modules
# # %load_ext autoreload
# # %autoreload 2
# For more info, see:
# https://ploomber.readthedocs.io/en/latest/user-guide/faq_index.html#auto-reloading-code-in-jupyter

# + tags=["parameters"]
upstream = ['new cases for GER']
product = None

# From: https://codereview.stackexchange.com/questions/92052/calculating-doubling-times-from-data-points
def doubling_time(m, x_pts, y_pts):
    window = 10

    x1 = x_pts[m]
    y1 = y_pts[m]
    x2 = x_pts[m+window]
    y2 = y_pts[m+window]

    return (x2 - x1) * log(2) / log(y2 / y1)

# +
number_of_days = 7
cases = pd.read_csv(upstream['new cases for GER']['data'], parse_dates=['date'])
cases = cases.set_index('date')
#cases = cases.cumsum()
cases = cases.rolling(7).mean()
aux = cases.shift(number_of_days)
aux = aux.dropna()

# +
cases['ratio'] = cases.new_cases / aux.new_cases
cases = cases.dropna()
cases['doubling_new_cases'] = np.log(cases['ratio']) #np.log( cases.new_cases / aux.new_cases )
cases['doubling_new_cases'] = (number_of_days-1) * log(2) / cases['doubling_new_cases']
cases = cases['doubling_new_cases']
#cases = cases.pad()

#+
cases.to_csv(product['data'])