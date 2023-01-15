# Author: Jose Lores Diz

import matplotlib.pyplot as plt
from matplotlib import rc
import econpizza as ep
import os
from utilities import _create_directory
import copy

# Control #

# Models
baseline = "./models/baseline_model.yaml"
dnwr = "./models/baseline_model_dnwr.yaml"
# lmodels = [baseline, dnwr]

# Shock
shk = ("e_beta", 0.02)
shockname = "positive_beta_shock"

# Variables to plot IRFs
variables = "y", "pi", "R", "w", "n", "k", "i", "c", "mc", "Rk"
var_names = (
    "Output",
    "Inflation",
    "Interest Rate",
    "Real Wages",
    "Labor",
    "Capital",
    "Investment",
    "Consumption",
    "Marginal Costs",
    "Rk",
)

# Solve and Plot #
# Load baseline
mod_b = ep.load(baseline)
_ = mod_b.solve_stst()
xSS = mod_b["stst"].copy()

# Load new model
mod_dnwr = ep.load(dnwr)
_ = mod_dnwr.solve_stst()
ySS = mod_dnwr["stst"].copy()

# Change Steady State inflation (CB's target)
dnwr_dict0 = ep.parse(dnwr)
dnwr_dict1 = copy.deepcopy(dnwr_dict0)
dnwr_dict1["steady_state"]["fixed_values"]["pi"] = 1
mod_dnwr2 = ep.load(dnwr_dict1)
_ = mod_dnwr2.solve_stst()
zSS = mod_dnwr2["stst"].copy()

# Find IRFs
x, flag_x = mod_b.find_path(shock=shk)
y, flag_y = mod_dnwr.find_path(shock=shk)
z, flag_z = mod_dnwr2.find_path(shock=shk)

# Find variables index
inds_b = [mod_b["variables"].index(v) for v in variables]
inds_dnwr = [mod_dnwr["variables"].index(v) for v in variables]
inds_dnwr2 = [mod_dnwr2["variables"].index(v) for v in variables]

# Directories for saving the plots
_create_directory(shockname)

# Plot #

# style
plt.rc("font", family="serif")
plt.rcParams["font.size"] = "14"

# produce the graphs
for i in range(len(variables)):
    fig, ax = plt.subplots(figsize=(8, 5))
    # plot as % deviation from Steady State
    ax.plot(
        (x[0:30, inds_b[i]] - xSS[variables[i]]) / xSS[variables[i]] * 100,
        marker="o",
        linestyle="-",
        label="baseline",
        color="tab:blue",
    )
    ax.plot(
        (y[0:30, inds_dnwr[i]] - ySS[variables[i]]) / ySS[variables[i]] * 100,
        marker="d",
        linestyle="-",
        label="dwnr 2% inflation target",
        color="tab:red",
    )
    ax.plot(
        (z[0:30, inds_dnwr[i]] - zSS[variables[i]]) / zSS[variables[i]] * 100,
        marker="^",
        linestyle="-",
        label="dwnr 0% inflation target",
        color="tab:green",
    )
    ax.set_title(var_names[i], size="18")
    ax.set_xlabel("Quarters")
    ax.set_ylabel("Percent")
    ax.legend()
    plt.savefig(f"bld/{shockname}/{var_names[i]}.pdf")
