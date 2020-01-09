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

def diagonal_averaging(hankel_matrix):
    '''Performs anti-diagonal averaging from given hankel matrix
    Returns: Pandas DataFrame object containing the reconstructed series'''
    mat = np.matrix(hankel_matrix)
    L, K = mat.shape
    L_star, K_star = min(L,K), max(L,K)
    new = np.zeros((L,K))
    if L > K:
        mat = mat.T
    ret = []
    
    #Diagonal Averaging
    for k in range(1-K_star, L_star):
        mask = np.eye(K_star, k=k, dtype='bool')[::-1][:L_star,:]
        mask_n = sum(sum(mask))
        ma = np.ma.masked_array(mat.A, mask=1-mask)
        ret+=[ma.sum()/mask_n]
    
    return df(ret).rename(columns={0:'Reconstruction'})