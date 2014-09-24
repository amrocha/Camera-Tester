# import all the stuff we need
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

df_data = pd.read_csv('file.csv')
print df_data

# x values
x_ax = np.linspace(0,9,10)

# now for each of the y values
y_cor = df_data['cor_pec']
y_mid = df_data['mid_pec']
y_per = df_data['per_pec']

plt.figure()
plt.axis([0, 10-1, 0, .145])

plt.plot(x_ax, y_cor,
         x_ax, y_mid,
         x_ax, y_per)

plt.xticks(x_ax, df_data['date'], size='small', rotation=70)
plt.tight_layout()
plt.savefig('normal_plot.png')

# new x values
xn_ax = np.linspace(0,9,10*10)

# new y values
yn_cor = interp1d(x_ax, y_cor, kind='cubic')
yn_mid = interp1d(x_ax, y_mid, kind='cubic')
yn_per = interp1d(x_ax, y_per, kind='cubic')

plt.figure()
plt.axis([0, 10-1, 0, .145])

plt.plot(xn_ax, yn_cor(xn_ax),
         xn_ax, yn_mid(xn_ax),
         xn_ax, yn_per(xn_ax))

plt.xticks(x_ax, df_data['date'], size='small', rotation=70)
plt.tight_layout()
plt.savefig('smooth_plot.png')