#!/usr/bin/env python
import socket
import logging
from threading import Thread


class LoggerListener(object):
    '''Listener that writes metrics to log'''
    def __init__(self, prefix):
        self.prefix = prefix
        self.logger = logging.getLogger("metrics")

    def submit(self, results):
        '''publish results to log'''
        for metric, value, timestamp in results:
            self.logger.info(
                "%s.%s\t%s\t%d" % (self.prefix, metric, value, timestamp))


class GraphiteListener(object):
    '''Listener that writes metrics to Graphite'''
    LOG = logging.getLogger('pt.graphite_listener')

    def __init__(self, prefix, address, port):
        self.address = address
        self.port = port
        self.prefix = prefix
        GraphiteListener.LOG.debug(
            "Created a Graphite listener with address = '%s', port = '%s', prefix = '%s'"
            % (address, port, prefix))

    def _submit_task(self, results):
        '''result submit task for threaded submitter'''
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.address, int(self.port)))
            for metric, value, timestamp in results:
                sock.sendall("%s.%s\t%s\t%d\n"
                    % (self.prefix, metric, value, timestamp))
            GraphiteListener.LOG.debug(
                "Sent metrics to %s:%s.", (self.address, self.port))
        except:
            GraphiteListener.LOG.exception(
                "Failed to send metrics to %s:%s.", self.address, self.port)
        finally:
            sock.close()

    def submit(self, results):
        '''publish results to Graphite'''
        GraphiteListener.LOG.debug(
            "Trying to send metrics to %s:%s...", self.address, self.port)
        Thread(target=self._submit_task, args=(results, )).start()
