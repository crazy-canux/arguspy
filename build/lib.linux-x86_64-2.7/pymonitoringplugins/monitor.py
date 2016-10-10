#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Basic functions for monitoring tools like nagios/icinga.

Copyright (C) 2016 Canux CHENG.
All rights reserved.
Name: monitor.py
Author: Canux CHENG canuxcheng@gmail.com
Version: V1.0.0.0
Time: Thu 28 Jul 2016 03:23:45 PM CST

Description:
    Test on nagios, naemon, icinga, shinken, centreon, opsview and sensu.
    [1.0.0.0] 20160728 init for basic function.
"""
import os
import sys
import logging
import argparse


class Monitor(object):

    """Basic class for monitor."""

    def __init__(self, name=None, version='1.0.0.0', description='Monitoring Plugin API'):
        """Init class monitor."""
        self.__name = os.path.basename(sys.argv[0]) if not name else name
        self.__version = version
        self.__description = description

        # Init the log
        logging.basicConfig(format='[%(levelname)s] (%(module)s) %(message)s')
        self.logger = logging.getLogger("monitor")
        self.logger.setLevel(logging.INFO)

        # Init the argument
        self.__define_options()
        self.define_sub_options()
        self.__parse_options()

        # Init the logger
        if self.args.debug:
            self.logger.setLevel(logging.DEBUG)
        self.logger.debug("===== BEGIN DEBUG =====")
        self.logger.debug("Init Monitor")

        # Init output data.
        self.output_ = ""
        self.shortoutput = ""
        self.longoutput = []
        self.perfdata = []

        # End the debug.
        if self.__class__.__name__ == "Monitor":
            self.logger.debug("===== END DEBUG =====")

    def __define_options(self):
        self.parser = argparse.ArgumentParser(description="Plugin for monitor.")
        self.parser.add_argument('-V', '--version',
                                 action='version',
                                 version='{0} {1}'.format(self.__name, self.__version),
                                 help='Show version')
        self.parser.add_argument('-D', '--debug',
                                 action='store_true',
                                 required=False,
                                 help='Show debug informations.',
                                 dest='debug')

    def define_sub_options(self):
        self.plugin_parser = self.parser.add_argument_group("Plugin Options",
                                                            "Options for all plugins.")
        self.plugin_parser.add_argument("-H", "--host",
                                        required=True,
                                        help="Host IP address or DNS",
                                        dest="host")
        self.plugin_parser.add_argument("-u", "--user",
                                        required=False,
                                        help="User name",
                                        dest="user")
        self.plugin_parser.add_argument("-p", "--password",
                                        required=False,
                                        help="User password",
                                        dest="password")

    def __parse_options(self):
        try:
            self.args = self.parser.parse_args()
        except Exception as e:
            self.unknown("parser args error: %s" % e)

    def output(self, substitute=None, long_output_limit=20):
        if not substitute:
            substitute = {}

        self.output_ += "{0}".format(self.shortoutput)
        if self.longoutput:
            self.output_ = self.output_.rstrip("\n")
            self.output_ += " | \n{0}".format(
                "\n".join(self.longoutput[:long_output_limit]))
            if long_output_limit:
                self.output_ += "\n(...showing only first {0} lines, " \
                    "{1} elements remaining...)".format(
                        long_output_limit,
                        len(self.longoutput[long_output_limit:]))
        if self.perfdata:
            self.output_ = self.output_.rstrip("\n")
            self.output_ += " | \n{0}".format(" ".join(self.perfdata))
        return self.output_.format(**substitute)

    def ok(self, msg):
        raise NagiosOk(msg)

    def warning(self, msg):
        raise NagiosWarning(msg)

    def critical(self, msg):
        raise NagiosCritical(msg)

    def unknown(self, msg):
        raise NagiosUnknown(msg)


class NagiosOk(Exception):

    def __init__(self, msg):
        print "OK - %s" % msg
        raise SystemExit(0)


class NagiosWarning(Exception):

    def __init__(self, msg):
        print "WARNING - %s" % msg
        raise SystemExit(1)


class NagiosCritical(Exception):

    def __init__(self, msg):
        print "CRITICAL - %s" % msg
        raise SystemExit(2)


class NagiosUnknown(Exception):

    def __init__(self, msg):
        print "UNKNOWN - %s" % msg
        raise SystemExit(3)
