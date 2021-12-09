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
upstream = ['active cases ger', 'total on ITS']
product = None
# -

active = pd.read_csv(upstream['active cases ger']['data'], parse_dates=['date'])
active = active.set_index('date')

its = pd.read_csv(upstream['total on ITS']['data'], parse_dates=['date'])
its = its.set_index('date')

# +
fig = plt.figure(figsize=(10, 8))

ax = plt.subplot(2, 1, 1)
ax.plot(active.index, active.active_cases)
ax.title.set_text('active infections')

ax = plt.subplot(2, 1, 2)
ax.plot(its.index, its.total_its, 'orange')
ax.title.set_text('on ITS')

plt.tight_layout()
fig.savefig(product['plot'], dpi=300)
# -