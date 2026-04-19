from Backend.BaseDataHandler import BaseDataHandler
from statistics import mean as stat_mean,median as stat_med,mode as stat_mode

class CentralTendencyCalculator(BaseDataHandler):
    def __init__(self):
        super().__init__() 

    def mean(self):
        return stat_mean(self.get_data_inputted())

    def median(self):
        return stat_med(self.get_data_inputted())

    def mode(self):
        return stat_mode(self.get_data_inputted())
