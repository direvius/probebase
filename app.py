#!/usr/bin/env python

#import sys

import daemon
import lockfile
import logging
import _globals as glob
from _listeners import LoggerListener, GraphiteListener
from _trackermanager import TrackerManager


class App(object):
    '''Application class. Parse options and serve requests'''
    def __init__(self, *probes):
        self.opts = glob.OPTIONS_PARSER.parse_args()[0]
        self.probes = probes
        if self.opts.verbose:
            log_level = logging.DEBUG
        else:
            log_level = logging.INFO
        logging.setLevel(log_level)
        # file logging
        fh = logging.FileHandler(self.opts.logfile)
        fh.setLevel(log_level)
        formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        fh.setFormatter(formatter)
        logging.addHandler(fh)
        # console logging
        if self.opts.interactive:
            sh = logging.StreamHandler()
            logging.addHandler(sh)

    def launch(self):
        if self.opts.interactive:
            self.run()
        else:
            self.daemonize()

    def run(self):
        '''main function'''
        if(self.opts.version):
            print 'process-tracker-1.6'
            return

        # initialize a tracker manager
        self.t_m = TrackerManager(int(self.opts.interval))
        # add listeners
        if(self.opts.log_enabled):
            self.t_m.add_listener(LoggerListener("metrics"))
        if self.opts.graphite:
            for address in self.opts.graphite_address.split(','):
                self.t_m.add_listener(
                    GraphiteListener(
                        self.opts.graphite_prefix,
                        address,
                        self.opts.graphite_port))
        # add probes
        self.t_m.add_probes(self.probes)
        try:
            raw_input("Press enter to stop...")
        except(SystemExit, KeyboardInterrupt):
            logging.info("Exiting, because interrupted.")
            break
        else:
            logging.exception("Unkown error")

    def daemonize(self):
        with(daemon.DaemonContext(
            detach_process=True,
            pidfile=lockfile.pidlockfile.PIDLockFile(
                "/var/run/process-tracker.pid"))):
            self.run()
