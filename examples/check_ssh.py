#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ssh plugins build with this library.

Copyright (C) 2016 Canux CHENG.
All rights reserved.
Name: check_ssh.py
Author: Canux CHENG canuxcheng@gmail.com
Version: V1.0.0
Time: Thu 28 Jul 2016 04:44:53 PM CST

Description:
    [1.0.0] 20160728 init for basic function.
"""
import sys

from arguspy.ssh_paramiko import Ssh


class Command(Ssh):

    """Run a command by SSH and return a single number."""

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.logger.debug("Init Command")

    def define_sub_options(self):
        super(Command, self).define_sub_options()
        self.cm_parser = self.subparsers.add_parser('command',
                                                    help='Run shell command.',
                                                    description='Options\
                                                    for command.')
        self.cm_parser.add_argument('-C', '--command',
                                    required=True,
                                    help='The shell command.',
                                    dest='command')
        self.cm_parser.add_argument('-w', '--warning',
                                    default=0,
                                    type=int,
                                    required=False,
                                    help='Warning value for Command, default is %(default)s',
                                    dest='warning')
        self.cm_parser.add_argument('-c', '--critical',
                                    default=0,
                                    type=int,
                                    required=False,
                                    help='Critical value for Command, default is %(default)s',
                                    dest='critical')

    def command_handle(self):
        """Get the number of the shell command."""
        self.__results = self.execute(self.args.command)
        self.close()

        self.logger.debug("results: {}".format(self.__results))
        if not self.__results:
            self.unknown("{} return nothing.".format(self.args.command))
        if len(self.__results) != 1:
            self.unknown("{} return more than one number.".format(self.args.command))
        self.__result = int(self.__results[0])
        self.logger.debug("result: {}".format(self.__result))
        if not isinstance(self.__result, (int, long)):
            self.unknown("{} didn't return single number.".format(self.args.command))

        status = self.ok
        # Compare the vlaue.
        if self.__result > self.args.warning:
            status = self.warning
        if self.__result > self.args.critical:
            status = self.critical

        # Output
        self.shortoutput = "{0} return {1}.".format(self.args.command, self.__result)
        [self.longoutput.append(line) for line in self.__results if self.__results]
        self.perfdata.append("{command}={result};{warn};{crit};0;".format(
            crit=self.args.critical,
            warn=self.args.warning,
            result=self.__result,
            command=self.args.command))

        # Return status with message to Nagios.
        status(self.output(long_output_limit=None))
        self.logger.debug("Return status and exit to Nagios.")


class Register(Command):

    """Register your own class here."""

    def __init__(self, *args, **kwargs):
        super(Register, self).__init__(*args, **kwargs)


def main():
    """Register your own mode and handle method here."""
    plugin = Register()
    arguments = sys.argv[1:]
    if 'command' in arguments:
        plugin.command_handle()
    else:
        plugin.unknown("Unknown actions.")

if __name__ == "__main__":
    main()
