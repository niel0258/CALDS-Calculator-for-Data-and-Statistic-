from Backend.CentralTendencyCalculator import CentralTendencyCalculator

class TestStatisticCalculator(CentralTendencyCalculator):
    def __init__(self):
        super().__init__() 

    def __zt_test(self, val_tested, z_or_t): 
        return (val_tested - self.mean()) / (z_or_t() / (len(self.get_data_inputted())) ** 0.5)

    def z_test(self,val_tested):
        return self.__zt_test(val_tested,self.population_std)

    def t_test(self,val_tested):
        return self.__zt_test(val_tested,self.sample_std)

    def get_df (self,num_subt):
        return len(self.get_data_inputted()) - num_subt
    