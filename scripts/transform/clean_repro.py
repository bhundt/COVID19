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

repro = pd.read_csv(upstream['download']['time_series_repro_germany'], parse_dates=['Datum'])
repro = repro.rename(columns={'Datum': 'date'})
repro = repro.set_index('date')
repro.to_csv(product['data'])