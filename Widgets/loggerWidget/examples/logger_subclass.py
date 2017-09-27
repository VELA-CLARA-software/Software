import logging
import sys
''' simple logger that takes the name of the current module '''
logger = logging.getLogger(__name__)

def test():
    ''' This will create some error messages for the logger '''
    logger.info('Hello from the subclass')
    logger.critical('Uh Oh!')

def main():
    pass

if __name__ == '__main__':
   main()
