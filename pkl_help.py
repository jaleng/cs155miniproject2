"""
Helper functions to deal with pkl objects
"""

import os.path
from sklearn.externals import joblib

def read_make_pkl(filename, generate_func, compress=False):
    """
    Get the saved object from pkl file, or if no file,
    generate the object, save it to file, and return
    the object
    """
    if (not os.path.isfile(filename)):
        print(filename +
              " object not stored. Creating and saving...")
        obj = generate_func()
        with open(filename, 'wb') as fo:
            joblib.dump(obj, fo, compress) # dump = store object to file
        return obj
    else:
        print(filename + " object was stored. Retrieving from file")
        with open(filename, 'rb') as fo:
            obj = joblib.load(fo) # load = load object from file
        return obj

def get_pkl(filename):
    with open(filename, 'rb') as fo:
        obj = joblib.load(fo)
        return obj
