from BaseDataHandler import BaseDataHandler
from CentralTendecyCalculator import CentralTendecyCalculator

class TestStatisticCalculator(BaseDataHandler,CentralTendecyCalculator):
    def __zt_test(self,val_tested,z_or_t):#1 means z, 2 means t

        return (val_tested - self.mean()) / (self.sd(mode) /( len(self.get_data()))**0.5)

    def z_test(self,val_tested):
        return self.__zt_test(val_tested,1)

    def t_test(self,val_tested):
        return self.__zt_test(val_tested,2)

    def get_df (self,num_subt):
        return len(self.get_data) - num_subt
    