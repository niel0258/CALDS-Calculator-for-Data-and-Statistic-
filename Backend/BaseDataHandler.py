#FATHER OF ALL CLASSES
from math import isnan

class BaseDataHandler():
    def __init__(self):
        self.__data_list = [0]
    
    def add_data(self, value):
        self.__data_list.append(value)
    
    def remove_data(self,index):
        self.__data_list.pop(index)

    def clear_data(self):
        self.__data_list.clear()

    #removes all the data that does not match the given data types
    #data types can be just one (e.g. int) or multiple (but must be inside a tuple(e.g. (int,float) )
    def remain_data_type(self,data_type):
        for i in range(len(self.__data_list)):
            if not isinstance(self.__data_list[i],data_type):
                self.remove_data(i)

    #replaces an element on a specific index
    #more recommended than add_data() on program where user can index  "out of range"
    def mod_data(self, index:int, data):
        if index >= len(self.__data_list):
            diff = index - len(self.__data_list)
            for i in range(diff - 1):
                self.__data_list.append(' ')

        self.__data_list[index] = data

    #replaces the whole data
    def replace_data(self,new_data):
        #new data must be an iteratable
        self.__data_list = new_data

    def get_data(self):
        return self.__data_list

    #ignores all nan values
    def __clean_data(self, list_of_data):
        cleaned_data = []
        for data in list_of_data:
            if (not isnan(data)):
                cleaned_data.append(data)
        print(f"Clean data: {cleaned_data}")
        return cleaned_data

    def get_data_inputted(self):
        return self.__clean_data(self.__data_list)