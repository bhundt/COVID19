# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import pandas as pd

# + tags=["parameters"]
upstream = ['new cases for GER', 'new deaths for GER']
product = None
number_sick_days = None
# -

# +
cases = pd.read_csv(upstream['new cases for GER']['data'])
deaths = pd.read_csv(upstream['new deaths for GER']['data'])
# -

aux = cases.merge(deaths, on='date', how='inner')
aux['new_recovered'] = aux['new_cases'].shift(number_sick_days) - aux['new_deaths'] # assumption: people are sick for this amount of time
aux = aux.dropna()
aux[['date', 'new_recovered']].to_csv(product['data'], index=False)