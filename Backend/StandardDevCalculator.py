from Backend.BaseDataHandler import BaseDataHandler
from scipy import stats

class StatDeviationCalculator(BaseDataHandler):

    def __init__(self):
        super().__init__()
        self._sample_std = None
        self._pop_std = None
        self.__data_memo = {}

    def __calc_std(self):
        data = tuple(self.get_data_inputted())

        if len(data) == 0:
            raise ValueError("No data available, please provide sufficient data.")

        # memoization key
        key = data

        if key in self.__data_memo:
            result = self.__data_memo[key]
        else:
            # standard deviation (sample)
            sample_std = stats.tstd(data, ddof=1)
            # standard deviation (population)
            pop_std = stats.tstd(data, ddof=0)
            result = (sample_std, pop_std)
            self.__data_memo[key] = result

        self._sample_std, self._pop_std = result

    def sample_std(self):
        self.__calc_std()
        return self._sample_std

    def population_std(self):
        self.__calc_std()
        return self._pop_std

    def both_std(self):
        self.__calc_std()
        return self._sample_std, self._pop_std
        