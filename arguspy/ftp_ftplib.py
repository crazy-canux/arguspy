#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Basic function for ftp build with python standard library ftplib.

Copyright (C) 2016 Canux CHENG.
All rights reserved.
Name: ftp_ftplib.py
Author: Canux CHENG canuxcheng@gmail.com
Version: V1.0.0
Time: Thu 28 Jul 2016 03:23:45 PM CST

Description:
    [1.0.0] 20160728 init for basic function.
"""
import ftplib

from super_devops.monitoring.nagios_wrapper import BaseNagios


class Ftp(BaseNagios):

    """Basic class for ftp."""

    def __init__(self):
        super(Ftp, self).__init__()
        self.logger.debug("Init Ftp")

        try:
            self.ftp = ftplib.FTP()
            self.ftp.connect(host=self.args.host,
                             port=self.args.port,
                             timeout=self.args.timeout)
            self.ftp.login(user=self.args.user,
                           passwd=self.args.password,
                           acct=self.args.acct)
            self.logger.debug("ftp connect succeed.")
        except Exception as e:
            self.unknown("Can not connect to the ftp: %s" % e)

    def connect(self):
        """Connect to ftp server."""
        return self.ftp

    def quit(self):
        """Close and exit the connection."""
        try:
            self.ftp.quit()
            self.logger.debug("quit connect succeed.")
        except ftplib.Error as e:
            self.unknown("quit connect error: %s" % e)

    def define_sub_options(self):
        super(Ftp, self).define_sub_options()
        self.ftp_parser = self.parser.add_argument_group("Ftp Options",
                                                         "options for ftp connect.")
        self.subparsers = self.parser.add_subparsers(title="Ftp Actions",
                                                     description="Action mode for ftp.",
                                                     dest='option',
                                                     help="Specify your action for ftp.")
        self.ftp_parser.add_argument('-P', '--port',
                                     default=21,
                                     type=int,
                                     required=False,
                                     help='ftp server port, default is %(default)s',
                                     dest='port')
        self.ftp_parser.add_argument('-t', '--timeout',
                                     default=-999,
                                     type=int,
                                     required=False,
                                     help='ftp timeout, default is %(default)s',
                                     dest='timeout')
        self.ftp_parser.add_argument('-a', '--acct',
                                     default='',
                                     required=False,
                                     help='acct for ftp login, default is %(default)s',
                                     dest='acct')
