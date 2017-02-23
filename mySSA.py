import numpy as np
import pandas as pd
from numpy import matrix as m
from pandas import DataFrame as df
from scipy import linalg
try:
    import seaborn
except:
    pass
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 16, 8

class mySSA(object):
    '''Singular Spectrum Analysis object'''
    def __init__(self, time_series):
        
        self.ts = pd.DataFrame(time_series)
        self.ts_name = self.ts.columns.tolist()[0]
        if self.ts_name==0:
            self.ts_name = 'ts'
        self.ts_v = self.ts.values
        self.ts_N = self.ts.shape[0]
        
    def embed(self, embedding_dimension=None, suspected_frequency=None, verbose=False):
        if not embedding_dimension:
            self.embedding_dimension = self.ts_N//2
        else:
            self.embedding_dimension = embedding_dimension
        if suspected_frequency:
            self.suspected_frequency = suspected_frequency
            self.embedding_dimension = (self.embedding_dimension//self.suspected_frequency)*self.suspected_frequency
    
        self.K = self.ts_N-self.embedding_dimension+1
        self.X = m(linalg.hankel(self.ts, np.zeros(self.embedding_dimension))).T[:,:self.K]
        self.X_df = df(self.X)
        self.X_complete = self.X_df.dropna(axis=1)
        self.X_com = m(self.X_complete.values)
        self.X_missing = self.X_df.drop(self.X_complete.columns, axis=1)
        self.X_miss = m(self.X_missing.values)
        self.trajectory_dimentions = self.X_df.shape
        self.complete_dimensions = self.X_complete.shape
        self.missing_dimensions = self.X_missing.shape
        self.no_missing = self.missing_dimensions[1]==0
            
        if verbose:
            msg1 = 'Embedding dimension\t:  {}\nTrajectory dimensions\t: {}'
            msg2 = 'Complete dimension\t: {}\nMissing dimension     \t: {}'
            msg1 = msg1.format(self.embedding_dimension, self.trajectory_dimentions)
            msg2 = msg2.format(self.complete_dimensions, self.missing_dimensions)
            self.printer('EMBEDDING SUMMARY', msg1, msg2)
    
    @staticmethod
    def printer(name, *args):
        print('-'*40)
        print(name+':')
        for msg in args:
            print(msg)  
    
    @staticmethod
    def dot(x,y):
        pass
    
    @staticmethod
    def get_contributions(X=None, s=None, plot=True):
        '''Calculate the relative contribution of each of the singular values'''
        lambdas = np.power(s,2)
        frob_norm = np.linalg.norm(X)
        ret = df(lambdas/(frob_norm**2), columns=['Contribution'])
        ret['Contribution'] = ret.Contribution.round(4)
        if plot:
            ax = ret[ret.Contribution!=0].plot.bar(legend=False)
            ax.set_xlabel("Lambda_i")
            ax.set_title('Non-zero contributions of Lambda_i')
            vals = ax.get_yticks()
            ax.set_yticklabels(['{:3.2f}%'.format(x*100) for x in vals])
            return ax
        return ret[ret.Contribution>0]
    
    @staticmethod
    def diagonal_averaging(hankel_matrix):
        '''Performs anti-diagonal averaging from given hankel matrix
        Returns: Pandas DataFrame object containing the reconstructed series'''
        mat = m(hankel_matrix)
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
        
    def decompose(self, verbose=False):
        X = self.X_com
        self.S = X*X.T
        self.U, self.s, self.V = linalg.svd(self.S)
        self.U, self.s, self.V = m(self.U), np.sqrt(self.s), m(self.V)
        self.d = np.linalg.matrix_rank(X)
        Vs, Xs, Ys, Zs = {}, {}, {}, {}
        for i in range(self.d):
            Zs[i] = self.s[i]*self.V[:,i]
            Vs[i] = X.T*(self.U[:,i]/self.s[i])
            Ys[i] = self.s[i]*self.U[:,i]
            Xs[i] = Ys[i]*(m(Vs[i]).T)
        self.Vs, self.Xs = Vs, Xs
        self.s_contributions = self.get_contributions(X, self.s, False)
        self.r = len(self.s_contributions[self.s_contributions>0])
        self.r_characteristic = round((self.s[:self.r]**2).sum()/(self.s**2).sum(),4)
        self.orthonormal_base = {i:self.U[:,i] for i in range(self.r)}
        
        if verbose:
            msg1 = 'Rank of trajectory\t\t: {}\nDimension of projection space\t: {}'
            msg1 = msg1.format(self.d, self.r)
            msg2 = 'Characteristic of projection\t: {}'.format(self.r_characteristic)
            self.printer('DECOMPOSITION SUMMARY', msg1, msg2)
    
    def view_s_contributions(self, adjust_scale=False, cumulative=False):
        contribs = self.s_contributions.copy()
        contribs = contribs[contribs.Contribution!=0]
        if cumulative:
            contribs['Contribution'] = contribs.Contribution.cumsum()
        if adjust_scale:
            contribs = (1/contribs).max()*1.1-(1/contribs)
        ax = contribs.plot.bar(legend=False)
        ax.set_xlabel("Singular_i")
        ax.set_title('Non-zero{} contribution of Singular_i {}'.\
                     format(' cumulative' if cumulative else '', '(scaled)' if adjust_scale else ''))
        if adjust_scale:
            ax.axes.get_yaxis().set_visible(False)
        vals = ax.get_yticks()
        ax.set_yticklabels(['{:3.0f}%'.format(x*100) for x in vals])
    
    @classmethod
    def view_reconstruction(cls, *hankel):
        '''Visualise the reconstruction of the hankel matrix/matrices passed to *hankel'''
        hankel_mat = None
        for han in hankel:
            if isinstance(hankel_mat,m):
                hankel_mat = hankel_mat + han
            else: 
                hankel_mat = han.copy()
        hankel_full = cls.diagonal_averaging(hankel_mat)
        hankel_full.plot(legend=False)
    
    def fill_missing(self, X=None):
        self.X_com_hat = np.zeros(self.complete_dimensions)
        self.verticality_coefficient = 0
        self.R = np.zeros(self.orthonormal_base[0].shape)[:-1]
        for Pi in self.orthonormal_base.values():
            self.X_com_hat += Pi*Pi.T*self.X_com
            pi = np.ravel(Pi)[-1]
            self.verticality_coefficient += pi**2
            self.R += pi*Pi[:-1]
        self.R = m(self.R/(1-self.verticality_coefficient))
        self.X_com_tilde = self.diagonal_averaging(self.X_com_hat)
        
    def recurrent_forecast(self, M):
        self.ts_forecast = np.array(self.ts_v[0])
        for i in range(1, self.ts_N+M):
            try:
                if np.isnan(self.ts_v[i]):
                    x = self.R.T*m(self.ts_forecast[max(0,i-self.R.shape[0]): i]).T
                    self.ts_forecast = np.append(self.ts_forecast,x[0])
                else:
                    self.ts_forecast = np.append(self.ts_forecast,self.ts_v[i])
            except(IndexError):
                x = self.R.T*m(self.ts_forecast[i-self.R.shape[0]: i]).T
                self.ts_forecast = np.append(self.ts_forecast, x[0])
            

if __name__=='__main__':
    from mySSA import mySSA
    from pandas import DataFrame as df
    import pandas as pd
    import numpy as np

    #Construct the data with gaps
    ts = pd.read_csv('AirPassengers.csv', parse_dates=True, index_col='Month')
    ts_ = ts.copy()
    ts_.ix[67:79] = np.nan
    ts_ = ts_.set_value('1961-12-01','#Passengers', np.nan).asfreq('MS')
    ssa_ = mySSA(ts_)

    ssa_.embed(embedding_dimension=36, suspected_frequency=12, verbose=True)
    ssa_.decompose(True)
    ssa_.view_s_contributions(adjust_scale=True)
    ssa_.view_reconstruction(*[ssa_.Xs[i] for i in range(13)])
    ssa_.fill_missing()