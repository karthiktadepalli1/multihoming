# Multihoming in Ridesharing Markets: Replication Archive

This repository will help replicate the calculations and figures created in our paper, [Multihoming in Ridesharing: Welfare and Investment.](https://www.karthiktadepalli.com/multihoming.pdf) The structure of the code is extremely simple: there are only two code files, and no raw data. The only assumption is that you have Python and R installed.

## `solve_equilibrium.py`

This script solves the numerical equilibrium in the ridesharing market, either for multihoming or singlehoming. It increments the efficiency parameter to trace how different values result in different equilibria. The result of these simulations is then exported to two CSV files, `single.csv` and `multi.csv`. Note that the special case where `alpha = 1` computes the symmetric equilibrium.

`solve_equilibrium.py` also serves to verify the calculations of equilibria in the appendices, including the solutions for Proposition 2, the threshold values for monopolization for Proposition 3, and the monopoly surpluses for Proposition 3.

## `figures.R`

This script takes as input the datasets `single.csv` and `multi.csv` and uses them to produce all the figures displayed in the paper. It is structured to highlight how each figure is produced, with explanations.
