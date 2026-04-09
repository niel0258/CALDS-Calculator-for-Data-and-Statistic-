from BaseDataHandler import BaseDataHandler
from statistics import mean as stat_mean,median as stat_med,mode as stat_mode

class CentralTendecyCalculator(BaseDataHandler):
    def mean(self,index):
        return stat_mean(self.data[index])

    def median(self,index):
        return stat_med(self.data[index])

    def mode(self,index):
        return stat_mode(self.data[index])