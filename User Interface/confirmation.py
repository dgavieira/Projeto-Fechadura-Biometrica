class Confirmation:
    def __init__(self,flag):
        self._flag = flag
    
    def get_flag(self):
        return self._flag
    
    def confirma(self, flag):
        if flag == True:
            return True
        else:
            return False
        