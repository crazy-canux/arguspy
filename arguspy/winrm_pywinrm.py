#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Basic function for Windows Remote Management build with third party library pywinrm.

Copyright (C) 2016 Canux CHENG.
All rights reserved.
Name: winrm_pywinrm.py
Author: Canux CHENG canuxcheng@gmail.com
Version: V1.0.0
Time: Thur 01 Aug 2016 04:43:40 PM CST

WinRM: Windows Remote Management.
Windows Remote Management (WinRM) is the Microsoft implementation of WS-Management Protocol,
a standard Simple Object Access Protocol (SOAP)-based,
firewall-friendly protocol that allows hardware and operating systems,
from different vendors, to interoperate.

Description:
    [1.0.0] 20160728 init for basic function.
"""
import winrm

from super_devops.monitoring.nagios_wrapper import BaseNagios


class WinRM(BaseNagios):

    """Basic class for WinRM."""

    def __init__(self):
        super(WinRM, self).__init__()
        self.logger.debug("Init WinRM")

        try:
            self.session = winrm.Session(self.args.host,
                                         auth=(self.args.domain + '\\' + self.args.user, self.args.password),
                                         transport=self.args.transport,
                                         service=self.args.service,
                                         server_cert_validation=self.args.scv,
                                         read_timeout_sec=self.args.rts,
                                         operation_timeout_sec=self.args.ots)
            self.logger.debug("winrm connect succeed.")
        except Exception as e:
            self.unknown("Connect by winrm error: %s" % e)

    def run_cmd(self, query):
        try:
            if query.split(",")[1:]:
                self.__result = self.session.run_cmd(str(query.split(",")[0]), query.split(",")[1:])
            else:
                self.__result = self.session.run_cmd(str(query))
            self.__return_code = self.__result.status_code
            self.__error = self.__result.std_err
            if self.__return_code:
                self.unknown("run command error: {}".format(self.__error))
            self.__output = self.__result.std_out
            return self.__output
        except Exception as e:
            self.unknown("run_cmd error: %s" % e)

    def run_ps(self, query):
        try:
            self.__result = self.session.run_ps(query)
            self.__return_code = self.__result.status_code
            self.__error = self.__result.std_err
            if self.__return_code:
                self.unknown("run powershell error: {}".format(self.__error))
            self.__output = self.__result.std_out
            return self.__output
        except Exception as e:
            self.unknown("run_ps error: %s" % e)

    def define_sub_options(self):
        super(WinRM, self).define_sub_options()
        self.wrm_parser = self.parser.add_argument_group("WinRM Options",
                                                         "options for winrm connect.")
        self.subparsers = self.parser.add_subparsers(title="WinRM Action",
                                                     description="Action mode for WinRM.",
                                                     dest="option",
                                                     help="Specify your action for WinRM.")
        self.wrm_parser.add_argument('-d', '--domain',
                                     required=False,
                                     help='wmi server domain.',
                                     dest='domain')
        self.wrm_parser.add_argument('--transport',
                                     default='ntlm',
                                     required=False,
                                     help='transport for winrm, default is %(default)s',
                                     dest='transport')
        self.wrm_parser.add_argument('--service',
                                     default='http',
                                     required=False,
                                     help='service for winrm, default is %(default)s',
                                     dest='service')
        self.wrm_parser.add_argument('--scv',
                                     default='ignore',
                                     required=False,
                                     help='server_cert_validation, default is %(default)s',
                                     dest='scv')
        self.wrm_parser.add_argument('--rts',
                                     default=30,
                                     type=int,
                                     help='read_timeout_sec, default is %(default)s',
                                     dest='rts')
        self.wrm_parser.add_argument('--ots',
                                     default=20,
                                     type=int,
                                     help='operation_timeout_sec, default is %(default)s',
                                     dest='ots')
