#!/usr/bin/env python
from probebase.app import AppBuilder
from os import getloadavg
from time import time
from itertools import izip


def probe_la():
    return ((metric, value, int(time()))
        for metric, value in izip(["la1", "la5", "la15"], getloadavg()))

AppBuilder(probe_la).create().launch()
