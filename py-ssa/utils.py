import numpy as np
import pandas as pd

def get_contributions(X=None, s=None, plot=True):
    '''Calculate the relative contribution of each of the singular values'''
    lambdas = np.power(s,2)
    frob_norm = np.linalg.norm(X)
    ret = pd.DataFrame(lambdas/(frob_norm**2), columns=['Contribution'])
    ret['Contribution'] = ret.Contribution.round(4)
    if plot:
        ax = ret[ret.Contribution!=0].plot.bar(legend=False)
        ax.set_xlabel("Lambda_i")
        ax.set_title('Non-zero contributions of Lambda_i')
        vals = ax.get_yticks()
        ax.set_yticklabels(['{:3.2f}%'.format(x*100) for x in vals])
        return ax
    return ret[ret.Contribution>0]