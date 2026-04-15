from Backend.BaseDataHandler import BaseDataHandler
from statistics import mean as stat_mean,median as stat_med,mode as stat_mode, pstdev as stat_pstdev, stdev as stat_stdev, variance as stat_svar, pvariance as stat_pvar

class CentralTendencyCalculator(BaseDataHandler):
    def __init__(self):
        super().__init__() 

    def mean(self):
        return stat_mean(self.get_data())

    def median(self):
        return stat_med(self.get_data())

    def mode(self):
        return stat_mode(self.get_data())

    #For Both items below: mode 1 is population and 2 is sample
    def sd(self,mode):
        if mode == 1:
            return stat_pstdev(self.get_data())
        else:
            return stat_stdev(self.get_data())

    def var(self,mode):
        if mode == 1:
            return stat_pvar(self.get_data())
        else:
            return stat_svar(self.get_data())
        