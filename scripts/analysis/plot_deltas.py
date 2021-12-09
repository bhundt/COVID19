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
import matplotlib.pyplot as plt

# + tags=["parameters"]
upstream = ['new cases for GER', 'new deaths for GER', 'recovered cases ger']
product = None
rolling_window = None
# -

cases = pd.read_csv(upstream['new cases for GER']['data'], parse_dates=['date'])
deaths = pd.read_csv(upstream['new deaths for GER']['data'], parse_dates=['date'])
recovered = pd.read_csv(upstream['recovered cases ger']['data'], parse_dates=['date'])

cases = cases.set_index('date')
deaths = deaths.set_index('date')
recovered = recovered.set_index('date')

cases_smoothed = cases.ewm(span=rolling_window).mean()
deaths_smoothed = deaths.ewm(span=rolling_window).mean()
recovered_smoothed = recovered.ewm(span=rolling_window).mean()


# +
fig = plt.figure(figsize=(10, 8))

ax = plt.subplot(3, 1, 1)
ax.plot(cases.index, cases.new_cases, 
            marker='.',
            markersize=1.5,
            linestyle='', 
            color='grey', 
            label='new cases')
ax.plot(cases_smoothed.index, cases_smoothed.new_cases, color='darkblue', label=f'new cases {rolling_window}-day EWM')
ax.title.set_text('new cases')

ax = plt.subplot(3, 1, 2)
ax.plot(recovered.index, recovered.new_recovered, 
            marker='.',
            markersize=1.5,
            linestyle='', 
            color='grey', 
            label='new recovered')
ax.plot(recovered_smoothed.index, recovered_smoothed.new_recovered, 'darkgreen', label=f'new recovered {rolling_window}-day EWM')
ax.title.set_text('new recovered')

ax = plt.subplot(3, 1, 3)
ax.plot(deaths.index, deaths.new_deaths, 
            marker='.',
            markersize=1.5,
            linestyle='', 
            color='grey', 
            label='new deaths')
ax.plot(deaths_smoothed.index, deaths_smoothed.new_deaths, 'k', label=f'new deaths {rolling_window}-day EWM')
ax.title.set_text('new deaths')

plt.tight_layout()
plt.savefig(product['plot'], dpi=300)
# -