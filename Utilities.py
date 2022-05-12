from shutil import get_terminal_size
from platform import python_implementation

def drawLine():
    if python_implementation() == 'PyPy':
        print('-' * get_terminal_size().columns)
    else:
        print(u'\u2500' * get_terminal_size().columns)