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
upstream = ['new cases for GER', 'new deaths for GER', 'recovered cases ger']
product = None
# -

# +
cases = pd.read_csv(upstream['new cases for GER']['data'])
deaths = pd.read_csv(upstream['new deaths for GER']['data'])
recovered = pd.read_csv(upstream['recovered cases ger']['data'])
# -

aux = cases.merge(deaths, on='date', how='inner')
aux = aux.merge(recovered, on='date', how='inner')

aux['active_cases'] = ( aux.new_cases.cumsum() 
                - aux.new_recovered.cumsum() 
                - aux.new_deaths.cumsum() )
aux = aux.drop(columns=['new_cases', 'new_recovered', 'new_deaths'])
aux.to_csv(product['data'], index=False)