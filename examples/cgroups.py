#!/usr/bin/python
from __future__ import with_statement
from os import walk
from time import time
from probebase.app import AppBuilder

CGROUPS_DIR = "/mnt/cgroups/memory"
CGROUPS_PREFIX_COUNT = len(CGROUPS_DIR.split('/'))
CGROUPS_STAT = "memory.stat"


def process_memory_file(dirname, filename):
    result = []
    prefix = '.'.join(dirname.split('/')[CGROUPS_PREFIX_COUNT:])
    with open("%s/%s" % (dirname, filename), 'r') as memoryfile:
        for line in memoryfile.readlines():
            metric, value = line.split()
            result.append(("cgroups.memory.%s.%s" % (prefix, metric), value, int(time())))
    return result


def probe_cgroups_memory():
    result = []
    for dirname, dirnames, filenames in walk(CGROUPS_DIR):
        for filename in filenames:
            if filename == CGROUPS_STAT:
                result.extend(process_memory_file(dirname, filename))
    return result


AppBuilder(probe_cgroups_memory).create().launch()
