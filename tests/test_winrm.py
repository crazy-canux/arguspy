#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test winrm with pywinrm.

Copyright (C) 2016 Canux CHENG.
All rights reserved.
Name: test_winrm.py
Author: Canux CHENG canuxcheng@gmail.com
Version: V1.0.0.0
Time: Thur 01 Aug 2016 04:43:40 PM CST

Description:
    [1.0.0.0] 20160728 init for basic function.
"""
import sys
import os

sys.path.insert(0, os.path.abspath('..'))
from winrm_pywinrm import WinRM


class SqlserverLocks(WinRM):

    """Check the attribute related to MSSQLSERVER_SQLServerLocks wmi class use WinRM."""

    def __init__(self):
        super(SqlserverLocks, self).__init__()
        self.logger.debug("Init SqlserverLocks")

    def define_sub_options(self):
        super(SqlserverLocks, self).define_sub_options()
        self.sl_parser = self.subparsers.add_parser('sqlserverlocks',
                                                    help='Options for SqlserverLocks',
                                                    description='All options for SqlserverLocks')
        self.sl_parser.add_argument('-q', '--query',
                                    required=False,
                                    help='cmd and powershell for winrm, like "ipconfig, /all"',
                                    dest='query')
        self.sl_parser.add_argument('-m', '--mode',
                                    required=True,
                                    help='From ["LockTimeoutsPersec", "LockWaitsPersec", "NumberofDeadlocksPersec"]',
                                    dest='mode')
        self.sl_parser.add_argument('-w', '--warning',
                                    default=0,
                                    type=int,
                                    required=False,
                                    help='Default is %(default)s',
                                    dest='warning')
        self.sl_parser.add_argument('-c', '--critical',
                                    default=0,
                                    type=int,
                                    required=False,
                                    help='Default is %(default)s',
                                    dest='critical')

    def sqlserverlocks_handle(self):
        self.ok_list = []
        self.warn_list = []
        self.crit_list = []
        status = self.ok

        self.__results = self.run_ps("""Get-WmiObject -Query "select * from Win32_PerfFormattedData_MSSQLSERVER_SQLServerLocks" | Format-List -Property Name,%s """ % self.args.mode)
        self.logger.debug("results: {}".format(self.__results))
        self.__results_list = self.__results.split()
        self.logger.debug("results list: {}".format(self.__results_list))
        # ['Name', ':', 'OibTrackTbl', 'LockTimeoutsPersec', ':', '0']
        self.__results_format_list = []
        [self.__results_format_list.append(value) for value in self.__results_list if value != ":" and value != "Name" and value != self.args.mode]
        self.logger.debug("results format list: {}".format(self.__results_format_list))
        # ['OibTrackTbl', '0', 'AllocUnit', '0', 'HoBT', '0', 'Metadata', '0']
        self.__results_format_dict = []
        for loop in range(0, len(self.__results_format_list)):
            if loop % 2 == 0:
                Name = self.__results_format_list[loop]
            else:
                Value = self.__results_format_list[loop]
                one_dict = {"Name": Name, self.args.mode: Value}
                self.__results_format_dict.append(one_dict)
        self.logger.debug("results format dict: {}".format(self.__results_format_dict))
        # [{'LockTimeoutsPersec': '0', 'Name': 'File'}, {'LockTimeoutsPersec': '0', 'Name': 'Database'}]

        for lock_dict in self.__results_format_dict:
            self.name = lock_dict.get('Name')
            self.logger.debug("name: {}".format(self.name))
            self.value = int(lock_dict.get(self.args.mode))
            self.logger.debug("value: {}".format(self.value))
            if self.value > self.args.critical:
                self.crit_list.append(self.name + " : " + self.value)
            elif self.value > self.args.warning:
                self.warn_list.append(self.name + " : " + self.value)
            else:
                self.ok_list.append(self.name + " : " + str(self.value))

        if self.crit_list:
            status = self.critical
        elif self.warn_list:
            status = self.warning
        else:
            status = self.ok

        self.shortoutput = "Found {0} {1} critical.".format(len(self.crit_list), self.args.mode)
        if self.crit_list:
            self.longoutput.append("===== Critical ====")
        [self.longoutput.append(filename) for filename in self.crit_list if self.crit_list]
        if self.warn_list:
            self.longoutput.append("===== Warning ====")
        [self.longoutput.append(filename) for filename in self.warn_list if self.warn_list]
        if self.ok_list:
            self.longoutput.append("===== OK ====")
        [self.longoutput.append(filename) for filename in self.ok_list if self.ok_list]
        self.perfdata.append("{mode}={result};{warn};{crit};0;".format(
            crit=self.args.critical,
            warn=self.args.warning,
            result=len(self.crit_list),
            mode=self.args.mode))

        # Return status and output to monitoring server.
        self.logger.debug("Return status and output.")
        status(self.output())


class Register(SqlserverLocks):

    """Register your own class here."""

    def __init__(self, *args, **kwargs):
        super(Register, self).__init__()


def test_winrm():
    """Register your own mode and handle method here."""
    plugin = Register()
    arguments = sys.argv[1:]
    if 'sqlserverlocks' in arguments:
        plugin.sqlserverlocks_handle()
    else:
        plugin.unknown("Unknown actions.")

if __name__ == "__main__":
    test_winrm()
