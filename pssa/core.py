import numpy as np
import pandas as pd
from scipy import linalg
import utils

try:
    import seaborn
except ModuleNotFoundError:
    pass


class SSA(object):
    """
    This is  a docstring
    """

    def __init__(self, time_series):
        self.ts = pd.DataFrame(time_series)
        self.ts_name = self.ts.columns.tolist()[0]
        if self.ts_name == 0:
            self.ts_name = "ts"
        self.ts_v = self.ts.values
        self.ts_n = self.ts.shape[0]
        self.freq = self.ts.index.inferred_freq

    def view_time_series(self):
        """
        Plot the time series
        """
        self.ts.plot(title="Original Time Series")

    def get_contributions(self):
        """
        Calculate the relative contribution of each of the singular values
        """
        return
        return utils.get_contributions(X, s, plot=False)

    def embed(self):
        """
        The embedding procedure transforms the initial time series into the sequence of L-dimensional lagged
        vectors {Xi}Ki=1, where K = N − L + 1.
        """
