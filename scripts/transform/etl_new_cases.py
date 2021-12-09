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
upstream = ['download']
product = None
# -

data = pd.read_csv(upstream['download']['time_series_covid19_confirmed_global'])
data = data[ data['Country/Region'] == 'Germany' ]
data = data.drop(columns=['Lat', 'Long', 'Province/State', 'Country/Region'])
data = data.transpose().reset_index()
data.columns = ['date', 'new_cases']
data.date = pd.to_datetime(data.date)
data['new_cases'] = data['new_cases'].diff()
data = data.dropna()
data = data.set_index('date')
data.to_csv(product['data'])