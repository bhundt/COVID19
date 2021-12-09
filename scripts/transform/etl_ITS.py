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

data = pd.read_csv(upstream['download']['time_series_its_germany'], parse_dates=['Datum'], sep=',')
data = data[ data['Behandlungsgruppe'] == "ERWACHSENE" ]
data.Datum = pd.to_datetime(data.Datum, utc=True).dt.date
data = data[['Datum', 'Aktuelle_COVID_Faelle_ITS']]
data.columns = ['date', 'total_its']
data = data.set_index('date')
data.to_csv(product['data'])
