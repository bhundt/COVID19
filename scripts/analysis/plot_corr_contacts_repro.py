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
#from scipy.stats import linregress
from scipy.optimize import curve_fit
import numpy as np
from datetime import date

# + tags=["parameters"]
upstream = ['download', 'clean repro ger']
product = None
# -

contacts = pd.read_csv(upstream['download']['time_series_contacts_germany'], parse_dates=['date'])
contacts = contacts.set_index('date')

repro = pd.read_csv(upstream['clean repro ger']['data'], parse_dates=['date'])
repro = repro.set_index('date')

contacts['CX_custom'] = contacts.k_7davg
contacts = contacts.shift(0) 

aux = contacts.merge(repro, on='date', how='inner')
aux = aux.dropna()

# the cutoff dates for the different waves in germany
dates = ['2020-1-1', '2020-7-1', '2021-2-15', '2021-7-1', date.today().strftime('%Y-%m-%d')]

# linear reg
def func(x, m):
    return m * x
params, _ = curve_fit(func, aux.loc[dates[1]:dates[4]].CX_custom, aux.loc[dates[1]:dates[4]].PS_7_Tage_R_Wert)
gradient = params[0]

# +
fig = plt.figure(figsize=(8, 5))

ax = plt.subplot(1, 1, 1)

# plot R==1.0 line
ax.plot([0, 20], [1, 1], 
        '--',
        color='gray',
        linewidth=0.4,
        label='critical R-value')

# plot data by wave
marker_options = ['o', 'd', '^', 's']
marker_colors = [(116,173,209), (254,224,144), (253,174,97), (244,109,67)]
for i, v in enumerate(dates[:-1]):
    ax.plot(aux.loc[dates[i]:dates[i+1]].CX_custom, aux.loc[dates[i]:dates[i+1]].PS_7_Tage_R_Wert, 
                marker=marker_options[i],
                markersize=3.0,
                linestyle='', 
                color=(marker_colors[i][0]/255, marker_colors[i][1]/255, marker_colors[i][2]/255), 
                label=f'data for wave {i+1}: {dates[i]}  -  {dates[i+1]}')

# plot lin reg
mn = np.min(aux.loc[dates[1]:dates[4]].CX_custom)
mx = np.max(aux.loc[dates[1]:dates[4]].CX_custom)
x1 = np.linspace(mn, mx, 500)
y1 = func(x1, gradient)
ax.plot(x1, y1, 
        '-',
        color=(215/255,40/255,38/255),
        linewidth=1.0,
        label=f'trend line (w/o wave 1): gradient={gradient:.2f}'
        )
ax.set_xlim([np.min(aux.CX_custom)-1, np.max(aux.CX_custom)+1])
ax.set_ylim([np.min(aux.PS_7_Tage_R_Wert-0.1), np.max(aux.PS_7_Tage_R_Wert) + 0.1])


# data sources
ax.text(ax.get_xlim()[0]+10 , ax.get_ylim()[0]-0.4, 'Plot: hundt.me. Data: RKI, Covid-19 Mobility Project', color='lightgray', fontsize=6)

ax.set_xlabel('daily number of contacts per person', color='gray', fontsize=10)
ax.set_ylabel('effective reproduction number', color='gray', fontsize=10)

# remove spines top and right
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# set spine color for remaining spines
ax.spines['bottom'].set_color('gray')
ax.spines['left'].set_color('gray')

[t.set_color('gray') for t in ax.get_yticklabels()]
[t.set_color('gray') for t in ax.get_xticklabels()]

# remove tick marks
ax.tick_params(axis=u'both', which=u'both',length=0)

plt.title('Impact of contact reduction on COVID-19 spreading (Germany)', 
            color='gray', 
            fontsize=13,
            y=1.04)

l = plt.legend(frameon=False, prop={'size': 8})
for text in l.get_texts():
    plt.setp(text, color = 'gray')

plt.tight_layout()
plt.savefig(product['plot'], dpi=300)
# -