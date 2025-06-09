"""
NeuroKit - A lightweight neural network library for Python.
"""

__version__ = "0.1.1"

# Use a try-except block to allow importing version without loading the full package
try:
    from .activations import *
    #from .convolution import Conv
    from .dense import Dense
    from .early_stopping import *
    from .losses import *
    #from .maxpool import MaxPooling
    from .metrics import *
    from .network import NeuralNetwork
    from .optimizer import *
    from .regularizer import *
    from .reshape import Reshape
except (ImportError, ModuleNotFoundError):
    # This allows importing just the version without requiring all dependencies
    pass
