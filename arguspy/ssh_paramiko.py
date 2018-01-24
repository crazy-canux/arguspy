#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Basic function for http/https build with third party library paramiko.

Copyright (C) 2016 Canux CHENG.
All rights reserved.
Name: ssh_paramiko.py
Author: Canux CHENG canuxcheng@gmail.com
Version: V1.0.0
Time: Thu 28 Jul 2016 04:44:53 PM CST

Description:
    [1.0.0] 20160728 init for basic function.
"""
import socket
import string

import paramiko

from monitor import Monitor
from super_devops.monitoring.nagios_wrapper import BaseNagios


class Ssh(BaseNagios):

    """Basic class for ssh."""

    def __init__(self):
        super(Ssh, self).__init__()
        self.logger.debug("Init Ssh")

        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(hostname=self.args.host,
                             port=self.args.port,
                             username=self.args.user,
                             password=self.args.password,
                             pkey=None,
                             key_filename=None,
                             timeout=self.args.timeout,
                             allow_agent=True,
                             look_for_keys=True,
                             compress=False,
                             sock=None)
            self.logger.debug("ssh connect succeed.")
        except paramiko.SSHException as e:
            self.unknown("Can not connect to server with SSH: %s" % e)

    def execute(self, command, timeout=None):
        """Execute a shell command."""
        try:
            self.channel = self.ssh.get_transport().open_session()
        except paramiko.SSHException as e:
            self.unknown("Create channel error: %s" % e)
        try:
            self.channel.settimeout(self.args.timeout if not timeout else timeout)
        except socket.timeout as e:
            self.unknown("Settimeout for channel error: %s" % e)
        try:
            self.logger.debug("command: {}".format(command))
            self.channel.exec_command(command)
        except paramiko.SSHException as e:
            self.unknown("Execute command error: %s" % e)
        try:
            self.stdin = self.channel.makefile('wb', -1)
            self.stderr = map(string.strip, self.channel.makefile_stderr('rb', -1).readlines())
            self.stdout = map(string.strip, self.channel.makefile('rb', -1).readlines())
        except Exception as e:
            self.unknown("Get result error: %s" % e)
        try:
            self.status = self.channel.recv_exit_status()
        except paramiko.SSHException as e:
            self.unknown("Get return code error: %s" % e)
        else:
            if self.status != 0:
                self.unknown("Return code: %d , stderr: %s" % (self.status, self.errors))
            else:
                return self.stdout
        finally:
            self.logger.debug("Execute command finish.")

    def close(self):
        """Close and exit the connection."""
        try:
            self.ssh.close()
            self.logger.debug("close connect succeed.")
        except paramiko.SSHException as e:
            self.unknown("close connect error: %s" % e)

    def define_sub_options(self):
        super(Ssh, self).define_sub_options()
        self.ssh_parser = self.parser.add_argument_group("SSH Options",
                                                         "options for SSH connect.")
        self.subparsers = self.parser.add_subparsers(title="SSH Actions",
                                                     description="Action mode for SSH.",
                                                     dest="option",
                                                     help="Specify your action for SSH.")
        self.ssh_parser.add_argument('-P', '--port',
                                     default='22',
                                     type=int,
                                     required=False,
                                     help='ssh server port, default is %(default)s.',
                                     dest='port')
        self.ssh_parser.add_argument('-t', '--timeout',
                                     default=60,
                                     type=int,
                                     required=False,
                                     help='ssh timeout, default is %(default)s',
                                     dest='timeout')
