from BaseDataHandler import BaseDataHandler
from scipy import stats

class StatRelationCalculator(BaseDataHandler):

    def __calcRel(self,other_data):
        self.__slope, self.__intercept, self.__r, self.__p, self.__std_err = stats.linregress(self.get_data,other_data)

    def linear_reg(self,other_data):
        self.__calcRel(other_data)
        return self.__slope
    def pearson_r(self,data):
        self.__calcRel(other_data)
        return self.__r
    
