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
import numpy as np
from scipy import signal

# + tags=["parameters"]
upstream = ['download', 'clean repro ger']
product = None
# -

contacts = pd.read_csv(upstream['download']['time_series_contacts_germany'], parse_dates=['date'])
contacts = contacts.set_index('date')

repro = pd.read_csv(upstream['clean repro ger']['data'], parse_dates=['date'])
repro = repro.set_index('date')

contacts.k_7davg = contacts.k_7davg.shift(0)
aux = contacts.merge(repro, on='date', how='inner')
aux = aux[['k_7davg', 'PS_7_Tage_R_Wert']]
#aux.k_7davg = aux.k_7davg.rolling(31).mean()
#aux.PS_7_Tage_R_Wert = aux.PS_7_Tage_R_Wert.rolling(31).mean()
aux = aux.dropna()

# +
# calculate signal correlation
corr = signal.correlate(aux.k_7davg.values, aux.PS_7_Tage_R_Wert.values)
lags = signal.correlation_lags(len(aux.k_7davg.values), len(aux.PS_7_Tage_R_Wert.values))
corr /= np.max(corr)

# +
fig = plt.figure(figsize=(8, 5))

ax = plt.subplot(1, 1, 1)

# plot corr data
ax.plot(lags, corr)
ax.set_xlim([-150, 150])

ax.set_xlabel('lag', color='gray', fontsize=10)
ax.set_ylabel('correlation', color='gray', fontsize=10)

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

plt.title('Cross-correlation betwenn contacts and reproduction number', 
            color='gray', 
            fontsize=13,
            y=1.04)

l = plt.legend(frameon=False, prop={'size': 8})
for text in l.get_texts():
    plt.setp(text, color = 'gray')

plt.tight_layout()
plt.savefig(product['plot'], dpi=300)
# -