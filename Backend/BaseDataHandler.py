#FATHER OF ALL CLASSES
class BaseDataHandler():
    __self.data_list = []

    def __init__(self):
        __self.data_list[0] = 0

    #Modifies data (takes the data group, the index of the data, if no data is passed then it removes data)
    def mod_data(self,index,data = None):
        self.data_list[index] = data