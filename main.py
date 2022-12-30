# Author: Jose Lores Diz

import matplotlib.pyplot as plt
import econpizza as ep
import os
from utilities import _create_directory

### Control ###

# Models 
baseline = 'baseline_model.yaml'
dnwr = 'baseline_model_dnwr.yaml'
#lmodels = [baseline, dnwr]

#Shock
shk = ('e_beta', 0.02)
shockname='postive_beta_shock'

#Variables to plot IRFs
variables = 'y', 'pi', 'R', 'w', 'n',  'k', 'i', 'c', 'mc', 'Rk'
var_names = 'Output', 'Inflation', 'Interest Rate', 'Real Wages', 'Labor', 'Capital', 'Investment', 'Consumption', 'Marginal Costs', 'Rk'

### Solve and Plot ###
# Load baseline
mod_b = ep.load(baseline)
_ = mod_b.solve_stst()
xSS = mod_b['stst'].copy()

# Load new model
mod_dnwr = ep.load(dnwr)
_ = mod_dnwr.solve_stst()
ySS = mod_dnwr['stst'].copy()

# Find IRFs
x, flag_x = mod_b.find_path(shock=shk)
y, flag_y = mod_dnwr.find_path(shock=shk)

# Find variables index
inds_b = [mod_b['variables'].index(v) for v in variables]
inds_dnwr = [mod_dnwr['variables'].index(v) for v in variables]

# Directories for saving the plots
_create_directory(shockname)

# Plot
for i in range(len(variables)):
    fig, ax = plt.subplots(figsize=(8, 4))
    #plot as % deviation from Steady State
    ax.plot((x[0:30,inds_b[i]]-xSS[variables[i]])/xSS[variables[i]]*100, marker='o',linestyle='-',label='baseline', color = 'b')  
    ax.plot((y[0:30,inds_dnwr[i]]-ySS[variables[i]])/ySS[variables[i]]*100, marker='d',linestyle='-',label = 'dwnr', color = 'r')
    ax.set_title(var_names[i])
    ax.set_xlabel('Quarters')  
    ax.set_ylabel('Percent')  
    ax.legend()
    plt.savefig(f'bld/{shockname}/{var_names[i]}.pdf')


