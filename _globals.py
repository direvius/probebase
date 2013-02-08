#!/usr/bin/env python

import socket
import string
from optparse import OptionParser


def parser_init():
    '''parse command line options'''
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
        default='five_sec.collectd.%s.p2p' % hostname
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

OPTIONS_PARSER = parser_init()
