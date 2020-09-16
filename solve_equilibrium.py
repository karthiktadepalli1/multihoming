"""
This script implements numerical computation of equilibrium in the models used in the paper, and exports the results to a data form for plotting.
"""

# ensure that packages are present, install if not
import os
os.system("pip install pandas numpy scipy")

# import packages
from scipy.optimize import fsolve, least_squares
import numpy as np
import pandas as pd
import math

# define the FOC equations of each asymmetric market, with a = 1 as an external starting parameter.
a = 1
def eq_single(vars):
    da, sa, db, sb = vars
    eq1 = 1 - 2*da - db - 2 * a * da / sa
    eq2 = da**2/(sa**2) - 2 * sa - sb
    eq3 = 1 - 2*db - da - 2 * db / sb
    eq4 = db**2/(sb**2) - 2 * sb - sa
    return([eq1, eq2, eq3, eq4])

def eq_multi(vars):
    da, sa, db, sb = vars
    eq1 = 1 - 2*da - db - (2 * a * da + db)/(sa + sb)
    eq2 = da * (a * da + db)/((sa + sb)**2) - a * (2 * sa + sb)
    eq3 = 1 - 2 * db - da - (a * da + 2 * db)/(sa + sb)
    eq4 = db * (a * da + db)/((sa + sb)**2) - sa - 2 * sb
    return([eq1, eq2, eq3, eq4])

# make dataframe to store results
single = pd.DataFrame(columns = ('alpha', 'd_1', 's_1', 'd_2', 's_2', 'pi_1', 'pi_2', 'type', 'nonneg'))
multi = pd.DataFrame(columns = ('alpha', 'd_1', 's_1', 'd_2', 's_2', 'pi_1', 'pi_2', 'type', 'nonneg'))

for i in range(5000):
    # singlehoming solution
    s = least_squares(eq_single, [1, 1, 1, 1], bounds = ((0, 0, 0, 0), (1, 1, 1, 1)))
    da, sa, db, sb = s['x']
    p1 = da * (1 - da - db - a * da/sa) - a * sa * (sa + sb)
    p2 = db * (1 - da - db - db/sb) - sb * (sa + sb)
    single.loc[i] = [a, da, sa, db, sb, p1, p2, 'single', s['success']]

    # multihoming solution
    m =  least_squares(eq_multi, [1, 1, 1, 1], bounds = ((0, 0, 0, 0), (1, 1, 1, 1)))
    da, sa, db, sb = m['x']
    p1 = da * (1 - da - db - (a * da + db)/(sa + sb))  - a * sa * (sa + sb)
    p2 = db * (1 - da - db - db/sb) - sb * (sa + sb)
    multi.loc[i] = [a, da, sa, db, sb, p1, p2, 'multi', m['success']]

    # decrement alpha for the next round
    a -= 0.0001

print(single)
print(multi)

single.to_csv('single.csv')
multi.to_csv('multi.csv')

# modified FOCs for the proof of Proposition 2, focusing on the derivatives s'(alpha), d'(alpha)

m = least_squares(eq_multi, [1, 1, 1, 1], bounds = ((0, 0, 0, 0), (1, 1, 1, 1)))
d, s = m['x']
D = np.sqrt(d**2 + 48 * s**3)

def eq_derivs(vars):
    dpr, spr = vars
    eq_dpr = d/2 + (36 * s**2 * spr - d**2)/(2 * D)
    eq_spr = (dpr * 4 * s * (1 + 2 * s) + 4 * d * s)/(3 * d)
    return([eq_dpr, eq_spr])

derivs = fsolve(eq_derivs, [0,0])
print(derivs)

dp, sp = derivs

def Dpr(sp2):
    return((d**2 + dp + 32 * (sp + sp2) * s**2 + 8 * s**2 * sp2)/D)

def eq2_derivs(vars):
    dpr, spr = vars
    eq_dpr2 = (-d - dp - Dpr(spr))/2
    eq_spr2 = - sp + (4 * s**2 * (dp + 2 * dpr) + 2 * s * (dp + d + 2 * dpr))/(3 * d)
    return([eq_dpr2, eq_spr2])

der2 = fsolve(eq2_derivs, [0, 0])
print(der2)

dp2, sp2 = der2

profit_der = - d * dp2 - d * (d + dp2)/(2 * s) + sp2 * d**2/(2 * s**2) - 2 * s**2 - s * sp2
print(profit_der)

# computing the shutdown points for each market structure

neg = single[single['pi_2'] < 0]
as_single = neg['alpha'].max()
neg = alpha[alpha['pi_2'] < 0]
as_multi = neg['alpha'].max()

# computing rider/driver surplus at the asymmetry-induced monopoly

alpha = as_multi
def eq_mono(vars):
    d, s = vars
    eq1 = 1 - 2 * d - 2 * alpha * d / s
    eq2 = d * d/(s * s) - 2 * s
    return([eq1, eq2])

def dets(a):
    global alpha
    alpha = a
    print(alpha)
    s = least_squares(eq_mono, [0.1, 0.1], bounds = ((0, 0), (1, 1)))
    d, s = s['x']
    print("d: {}".format(d))
    print("s: {}".format(s))
    print("Profit: {}".format(d - d*d - a * d * d/s - a * s * s))
    print("RS: {}".format(a * d * d / (2 * s) + d * d/2))
    print("DS: {}".format(2 * a * s * s * s/(3 * d)))

print("\nSINGLEHOMING\n")
dets(as_single)
print("\nMULTIHOMING\n")
dets(as_multi)
