import sys

import theano
import numpy as np


__all__ = ('format_data', 'is_layer_accept_1d_feature', 'asfloat',
           'AttributeKeyDict', 'is_int_array')


def format_data(data, is_feature1d=True, copy=False):
    """ Transform data in a standardized format.

    Notes
    -----
    It should be applied to the input data prior to use in
    learning algorithms.

    Parameters
    ----------
    data : array-like
        Data that should be formated. That could be, matrix, vector or
        Pandas DataFrame instance.
    is_feature1d : bool
        Should be equal to ``True`` if input data if a vector that
        contains n samples with 1 feature each. Defaults to ``True``.
    copy : bool
        Defaults to ``False``.

    Returns
    -------
    ndarray
        The same input data but transformed to a standardized format
        for further use.
    """
    if data is None:
        return

    data = np.array(asfloat(data), copy=copy)

    # Valid number of features for one or two dimentions
    n_features = data.shape[-1]
    if 'pandas' in sys.modules:
        pandas = sys.modules['pandas']

        if isinstance(data, (pandas.Series, pandas.DataFrame)):
            data = data.values

    if data.ndim == 1:
        data_shape = (n_features, 1) if is_feature1d else (1, n_features)
        data = data.reshape(data_shape)

    return data


def is_layer_accept_1d_feature(layer):
    return (layer.input_size == 1)


def asfloat(value):
    """ Convert variable to float type configured by theano
    floatX variable.

    Parameters
    ----------
    value : matrix, ndarray or scalar
        Value that could be converted to float type.

    Returns
    -------
    matrix, ndarray or scalar
        Output would be input value converted to float type
        configured by theano floatX variable.
    """

    if isinstance(value, (np.matrix, np.ndarray)):
        return value.astype(theano.config.floatX)

    float_x_type = np.cast[theano.config.floatX]
    return float_x_type(value)


class AttributeKeyDict(dict):
    """ Modified built-in Python ``dict`` class. That modification
    helps get and set values like attributes.

    Exampels
    --------
    >>> attrdict = AttributeKeyDict()
    >>> attrdict
    {}
    >>> attrdict.test_key = 'test_value'
    >>> attrdict
    {'test_key': 'test_value'}
    >>> attrdict.test_key
    'test_value'
    """

    def __getattr__(self, attrname):
        return self[attrname]

    def __setattr__(self, attrname, value):
        self[attrname] = value

    def __delattr__(self, attrname):
        del self[attrname]


def is_int_array(sequence):
    """ Check that sequence contains only integer numbers.

    Parameters
    ----------
    sequence : list, tuple
        Array that should be validated.

    Returns
    -------
    bool
        Result would be ``True`` only if each element in a sequence contains
        is an integer. ``False`` otherwise.
    """
    return all(isinstance(element, int) for element in sequence)
