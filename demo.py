# from src.logger import logging          # ok so why importing logging instead of configurtion func
#     # well the moment when we import src.logger then pyhton will auto execute the line by line of that logger module(any dir that have __init__.py) become a module
#     # python logging have global nature just define 


# logging.debug('Debug message')
# logging.error('Error message')
# logging.warning('Warning message')
# logging.critical('Critical message')
# logging.info('A Info message')




# from src.logger import logging
# from src.exception import exceptions
# import sys

# try: 
#     1+'str'
# except Exception as e:
#     logging.info(e)
#     raise exceptions(e,sys) from e 





from src.pipline.training_pipeline import TrainPipeline

pipeline = TrainPipeline()
pipeline.run_pipeline()

