from StatRelationCalculator import StatRelationCalculator
from CentralTendecyCalculator import CentralTendecyCalculator

class DataHandler(CentralTendecyCalculator,StatRelationCalculator):
    def __init__(self):
        pass

    def add_data(self,value):
        if not isinstance(value, (int, float)):
            raise ValueError("Only numeric values allowed")
        self._data_list.append(value)

    def mod_data(self, index, data):
        #error handle
        if not (isinstance(data,(float,int))):
            return

        if index >= len(self.__data_list):
            diff = index - len(self.__data_list)
            for i in range(diff - 1):
                self.__data_list.append(' ')

        self.__data_list[index] = data
