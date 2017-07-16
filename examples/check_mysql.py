#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Mysql plugins build with this library.

Copyright (C) 2016 Canux CHENG.
All rights reserved.
Name: check_mysql.py
Author: Canux CHENG canuxcheng@gmail.com
Version: V1.0.0
Time: Wed 27 Jul 2016 02:32:05 PM CST

Description:
    [1.0.0] 20160727 Init this plugin for basic functions.
"""
import sys

from arguspy.mysql_pymysql import Mysql


class Sql(Mysql):

    """Just for the return value is a single number."""

    def __init__(self, *args, **kwargs):
        super(Sql, self).__init__(*args, **kwargs)
        self.logger.debug("Init Sql")

    def define_sub_options(self):
        super(Sql, self).define_sub_options()
        self.sql_parser = self.subparsers.add_parser('sql',
                                                     help='Run sql/SP.',
                                                     description='Options\
                                                     for sql/SP.')
        self.sql_parser.add_argument('-s', '--sql',
                                     action='append',
                                     type=str,
                                     required=True,
                                     help='The sql or store procedure.',
                                     dest='sql')
        self.sql_parser.add_argument('-w', '--warning',
                                     default=0,
                                     type=int,
                                     required=False,
                                     help='Warning value for sql, default is %(default)s',
                                     dest='warning')
        self.sql_parser.add_argument('-c', '--critical',
                                     default=0,
                                     type=int,
                                     required=False,
                                     help='Critical value for sql, default is %(default)s',
                                     dest='critical')

    def sql_handle(self):
        self.__results = self.query(self.args.sql)
        self.close()
        self.logger.debug("results: {}".format(self.__results))
        if not self.__results:
            self.unknown("SP/SQL return nothing.")
        if len(self.__results) != 1:
            self.unknown("SP/SQL return more than one number.")
        self.__result = self.__results[0][0]
        if not isinstance(self.__result, (int, long)):
            self.unknown("SP/SQL not return a single number.")
        self.logger.debug("result: {}".format(self.__result))
        status = self.ok

        # Compare the vlaue.
        if self.__result > self.args.warning:
            status = self.warning
        if self.__result > self.args.critical:
            status = self.critical

        # Output
        self.shortoutput = "The result is {}".format(self.__result)
        self.longoutput.append("-------------------------------\n")
        self.longoutput.append(str(self.__results))
        self.longoutput.append("-------------------------------\n")
        self.perfdata.append("\n{sql}={result};{warn};{crit};0;".format(
            crit=self.args.critical,
            warn=self.args.warning,
            result=self.__result,
            sql=self.args.sql))

        # Return status with message to Nagios.
        status(self.output(long_output_limit=None))
        self.logger.debug("Return status and exit to Nagios.")


class Register(Sql):

    """Register your own class here."""

    def __init__(self, *args, **kwargs):
        super(Register, self).__init__(*args, **kwargs)


def main():
    """Register your own mode and handle method here."""
    plugin = Register()
    arguments = sys.argv[1:]
    if 'sql' in arguments:
        plugin.sql_handle()
    else:
        plugin.unknown("Unknown actions.")

if __name__ == "__main__":
    main()
