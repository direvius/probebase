#!/usr/bin/env python
from apscheduler.scheduler import Scheduler
from time import time
import logging


class TrackerManager(object):
    '''Manages process information collection for multiple processes'''
    LOG = logging.getLogger('pt.tracker_manager')

    def __init__(self, interval, yabs_host):
        TrackerManager.LOG.debug(
            "Initializing TrackerManager with interval = %s",
            interval)
        self.listeners = []
        self.probes = []
        self.scheduler = Scheduler()
        self.scheduler.add_interval_job(self.tracking_job, seconds=interval)
        self.scheduler.start()

    def add_listener(self, listener):
        '''Add listener that will receive metrics'''
        self.listeners.append(listener)

    def add_probe(self, probe):
        '''Add probe that will collect metrics'''
        self.probes.append(probe)

    def tracking_job(self):
        '''a job that monitors'''
        results = [probe() for probe in self.probes]
        self.submit(results)

    def submit(self, results):
        '''publish results to listeners'''
        for listener in self.listeners:
            listener.submit(results, time())
