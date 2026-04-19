from Backend.BaseDataHandler import BaseDataHandler
from scipy import stats

class StatRelationCalculator(BaseDataHandler):
    def __init__(self):
        super().__init__()
        self._slope = None
        self._intercept = None
        self._r = None
        self._p = None
        self._std_err = None
        self.__data_memo = {}

    def __calc_rel(self, other_data):
        if other_data is None:
            return 0
        
        x_data = tuple(self.get_data_inputted())
        y_data = tuple(other_data)#must pass a "clean" tuple, meaning no nan values 
        
        # Store data in memo
        key = (x_data, y_data)
        
        # Avoids recalculation
        if key in self.__data_memo:
            result = self.__data_memo[key]
        else:
            result = stats.linregress(x_data, y_data)
            self.__data_memo[key] = result
        
        self._slope = result.slope
        self._intercept = result.intercept
        self._r = result.rvalue
        self._p = result.pvalue
        self._std_err = result.stderr

    def linear_reg(self, other_data):
        self.__calc_rel(other_data)
        return self._slope, self._intercept

    def calc_possible_y(self, x_input, other_data):
        self.__calc_rel(other_data)
        return self._slope * x_input + self._intercept

    def pearson_r(self, other_data):
        self.__calc_rel(other_data)
        return self._r