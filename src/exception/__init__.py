import sys    # to extract error info
import logging


def error_message_details(error: Exception, error_detail:sys) -> str:
        """
    Extracts detailed error information including file name, line number, and the error message.

    :param error: The exception that occurred.
    :param error_detail: The sys module to access traceback details.
    :return: A formatted error message string.
    """
        

        # extract traceback details 
        _,_, exp_information = error_detail.exc_info()

        # extracting the filename & line no where error occured
        file_name = exp_information.tb_frame.f_code.co_filename
        line_no = exp_information.tb_lineno

        #create a formatted error message as str with file_name, line no and the error
        error_message = f'Error occured in this .Py file {file_name} at line no {line_no} , Error --> {str(error)}'

        # log the error
        logging.error(error_message)

        return error_message


class exceptions(Exception):
        def __init__(self, error:str, error_detail:sys):
                
                # calling base/parent constructor so that Exception constuctor store error attribute 
                super().__init__(error)
                self.error = error_message_details(error, error_detail)

        def __str__(self):
                "To convert error traceback to error"
                return self.error
