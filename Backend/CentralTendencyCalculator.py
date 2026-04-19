from Backend.StandardDevCalculator import StatDeviationCalculator
from statistics import mean as stat_mean,median as stat_med,mode as stat_mode

class CentralTendencyCalculator(StatDeviationCalculator):
    def __init__(self):
        super().__init__() 

    def mean(self):
        return stat_mean(self.get_data_inputted())

    def median(self):
        return stat_med(self.get_data_inputted())

    def mode(self):
        return stat_mode(self.get_data_inputted())
