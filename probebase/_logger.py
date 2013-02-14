#!/usr/bin/env python
import logging
import inspect
from time import time
from functools import wraps


def trace(fn):
    varList, _, _, default = inspect.getargspec(fn)
    args_values = {}
    if default is not None:
        args_values = dict((varList[-len(default):][i], v)
            for i, v in enumerate(default))

    @wraps(fn)
    def _trace(*argt, **argd):
        args_values.update(dict((varList[i], v) for i, v in enumerate(argt)))
        args_values.update(argd)

        params = '; '.join('%s = %s' % (arg, value)
            for arg, value in args_values.iteritems())
        logging.debug('i> %s | %s', fn.__name__, params)
        ret = fn(*argt, **argd)
        logging.debug('o< %s | %s', fn.__name__, ret)
        return ret
    return _trace


def measure(fn):
    @wraps(fn)
    def _measure(*argt, **argd):
        start = time()
        ret = fn(*argt, **argd)
        diff = time() - start
        logging.debug('%s: %s ms', fn.__name__, int(diff * 1000))
        return ret
    return _measure
