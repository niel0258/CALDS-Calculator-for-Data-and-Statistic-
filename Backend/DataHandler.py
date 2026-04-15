from Backend.StatRelationCalculator import StatRelationCalculator
from Backend.TestStatistic import TestStatisticCalculator
import pandas as pd

class DataHandler(StatRelationCalculator,TestStatisticCalculator):
    def __init__(self,data_name):
        super().__init__() 
        #needs a data name
        self._data_name = data_name

    #just adds an error check
    def add_data(self,value):
        if not isinstance(value, (int, float)):
            raise ValueError("Only numeric values allowed")
        self._data_list.append(value)

    def mod_data(self, index:int, data):
        data_list = self.get_data()

        #error handle
        if not (isinstance(data,(float,int))):
            raise ValueError("Only numeric values allowed")

        if index >= len(data_list):
            diff = index - len(data_list)
            for i in range(diff+1):#add 1 to add padding
                data_list.append(0)

        data_list[index] = data

        print(data_list)

    def get_data_name(self):
        return self._data_name
    
    def import_data(self,path:str):
        df = pd.read_csv(path)
        #Column must match data name
        return self.replace_data(df[self._data_name].to_list())
    
    #params(path:file path,other_datas: tuple of data you want to cram on one file)
    def export_data(self,path:str,other_datas:tuple = None):
        export_list = [pd.DataFrame(data.get_data(), columns=[data.get_data_name()])]
        
        if other_datas == None:
            export_list[0].to_csv(path)
        else:
            #extends the list to add all the other_data
            export_list.extend([pd.DataFrame(data,columns=data.get_data_name()) for data in other_datas])
            pd.concat(export_list,axis=0).to_csv(path,index=False)
