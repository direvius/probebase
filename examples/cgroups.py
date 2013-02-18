#!/usr/bin/python
from __future__ import with_statement
from os import walk
from time import time
from probebase.app import AppBuilder

CGROUPS_DIR = "/mnt/cgroups/memory"
CGROUPS_PREFIX_COUNT = len(CGROUPS_DIR.split('/'))
CGROUPS_STAT = "memory.stat"


def process_memory_file(filename):
    result = []
    prefix = '.'.join(filename.split('/')[CGROUPS_PREFIX_COUNT:])
    with open(filename, 'r') as memoryfile:
        for line in memoryfile.readlines():
            metric, value = line.split()
            result.append(("%s.%s" % (prefix, metric), value, int(time())))
    return result


def probe_cgroups_memory():
    result = []
    for dirname, dirnames, filenames in walk(CGROUPS_DIR):
        for filename in filenames:
            if filename == CGROUPS_STAT:
                result.extend(process_memory_file("%s/%s" % (dirname, filename)))
    return result


AppBuilder(probe_cgroups_memory).create().launch()
