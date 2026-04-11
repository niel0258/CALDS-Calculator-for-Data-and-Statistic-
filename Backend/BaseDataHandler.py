#FATHER OF ALL CLASSES
class BaseDataHandler():
    def __init__(self):
        self.__data_list = [0]

    def mod_data(self, index, data):
        if not isinstance(data,(int,float)):
            return

        if index < 0:
            raise IndexError("Index out of range")
        
        if index >= len(self.__data_list):
            diff = index - len(self.__data_list)
            for i in range(diff - 1):
                self.__data_list.append(0)

        self.__data_list[index] = data

    def get_data(self):
        return self.__data_list