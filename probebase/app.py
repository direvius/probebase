#!/usr/bin/env python

from __future__ import with_statement
import daemon
import lockfile
import logging
from _listeners import LoggerListener, GraphiteListener
from _trackermanager import TrackerManager
import socket
from optparse import OptionParser
import string


class AppBuilder(object):
    @staticmethod
    def default_parser():
        '''get default command line options parser'''
        argparser = OptionParser()

        argparser.add_option('-l', '--log',
            help='enable logging metrics',
            action='store_true',
            dest='log_enabled',
            default=False
            )
        argparser.add_option('-L', '--log-file',
            help='log file',
            dest='logfile',
            default='./probe.log'
            )
        argparser.add_option('-r', '--graphite-address',
            help='graphite server address (use comma for multiple addresses)',
            dest='graphite_address',
            default='localhost'
            )
        argparser.add_option('-R', '--graphite-port',
            help='graphite server port',
            dest='graphite_port',
            default='2024'
            )
        argparser.add_option('-i', '--interval',
            help='collection interval in seconds',
            dest='interval',
            default='5'
            )
        hostname = socket.getfqdn().translate(string.maketrans(".", "_"))
        argparser.add_option('-P', '--graphite-prefix',
            help='graphite prefix',
            dest='graphite_prefix',
            default='five_sec.%s' % hostname
            )
        argparser.add_option("-g", "--use-graphite",
            help="report metrics to graphite",
            action="store_true",
            dest="graphite",
            default=False
            )
        argparser.add_option("-v", "--version",
            help="show version and exit",
            action="store_true",
            dest="version",
            default=False
            )
        argparser.add_option("-V", "--verbose",
            help="set log level to DEBUG",
            action="store_true",
            dest="verbose",
            default=False
            )
        argparser.add_option("-I", "--interactive",
            help="do not detach from console",
            action="store_true",
            dest="interactive",
            default=False
            )
        return argparser

    def __init__(self, *probes):
        self.probes = probes
        self.argparser = AppBuilder.default_parser()

    def add_option(self, *args, **kw_args):
        self.argparser.add_option(*args, **kw_args)
        return self

    def create(self):
        return App(self.argparser.parse_args()[0], self.probes)


class App(object):
    '''Application class. Parse options and serve requests'''
    def __init__(self, opts, probes):
        self.opts = opts
        self.probes = probes
        self.logger = logging.getLogger()
        if self.opts.verbose:
            log_level = logging.DEBUG
        else:
            log_level = logging.INFO
        self.logger.setLevel(log_level)
        # file logging
        fh = logging.FileHandler(self.opts.logfile)
        fh.setLevel(log_level)
        formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        # console logging
        if self.opts.interactive:
            sh = logging.StreamHandler()
            sh.setLevel(log_level)
            self.logger.addHandler(sh)

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
            self.t_m.add_listener(LoggerListener(self.opts.graphite_prefix))
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
        else:
            logging.exception("Unkown error")

    def daemonize(self):
        with(daemon.DaemonContext(
            detach_process=True,
            pidfile=lockfile.pidlockfile.PIDLockFile(
                "/var/run/process-tracker.pid"))):
            self.run()
