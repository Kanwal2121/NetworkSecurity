import sys
from networksecurity.logging import logger
class NetworkSecurityException(Exception):
    def __init__(self,error,error_detail:sys):
        self.error_message=error
        _,_,exc_tb=error_detail.exc_info()
        self.line_no=exc_tb.tb_lineno
        self.file_name=exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return "Error accoured in python script name [{0}],lineno [{1}],error_message[{2}] ".format(self.file_name,self.line_no,str(self.error_message))
    


        
        