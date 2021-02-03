from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# from .custom_setup import __setup__
# __setup__()

import os
from .main import GetStockCode
from .main import GetStockData
from .main import StockData
from .main import NaverReader
from .main import FastReader
from .main import SaveCSV

__version__ = '0.0.1'
__doc__ = None
__name__ = 'Finance'
__path__ = os.getcwd()

__all__ = ['__version__', 
		   '__doc__', 
		   '__name__',
		   '__path__',
		   'GetStockCode', 
		   'GetStockData',
		   'StockData',
		   'SaveCSV',
		   'NaverReader',
		   'FastReader']