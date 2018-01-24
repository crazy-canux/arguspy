#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Basic function for MicroSoft Sql Server Database build with third party library pymssql.

Copyright (C) 2016 Canux CHENG.
All rights reserved.
Name: mssql_pymssql.py
Author: Canux CHENG canuxcheng@gmail.com
Version: V1.0.0
Time: Wed 27 Jul 2016 02:01:20 PM CST

Description:
    [1.0.0] 20160727 Init this plugin for basic functions.
"""
import pymssql

from monitor import Monitor
from super_devops.monitoring.nagios_wrapper import BaseNagios


class Mssql(BaseNagios):

    """Basic class for mssql."""

    def __init__(self):
        super(Mssql, self).__init__()
        self.logger.debug("Init Mssql")

        try:
            self.conn = pymssql.connect(server=self.args.host,
                                        user=self.args.user,
                                        password=self.args.password,
                                        database=self.args.database,
                                        timeout=self.args.timeout,
                                        login_timeout=self.args.login_timeout,
                                        charset=self.args.charset,
                                        as_dict=self.args.as_dict)
            self.logger.debug("Mssql connect succeed.")
        except pymssql.Error as e:
            self.unknown("Can not connect to the mssql: %s" % e)

    def query(self, sql_query):
        try:
            self.cursor = self.conn.cursor()
            self.logger.debug("get cursor ok")
        except pymssql.Error as e:
            self.unknown("Get cursor error: %s" % e)
        try:
            self.logger.debug("sql: {}".format("".join(sql_query)))
            self.cursor.execute("".join(sql_query))
            self.logger.debug("execute ok")
        except pymssql.Error as e:
            self.unknown("Execute sql error: %s" % e)
        try:
            self.results = self.cursor.fetchall()
            self.logger.debug("fetchall ok")
        except pymssql.Error as e:
            self.unknown("Fetchall error: %s" % e)
        try:
            self.cursor.close()
            self.logger.debug("Close cursor ok")
        except pymssql.Error as e:
            self.unknown("Close cursor error: %s" % e)
        return self.results

    def close(self):
        """Close the connection."""
        try:
            self.conn.close()
            self.logger.debug("Close connect succeed.")
        except pymssql.Error as e:
            self.unknown("Close connect error: %s" % e)

    def define_sub_options(self):
        super(Mssql, self).define_sub_options()
        self.mssql_parser = self.parser.add_argument_group("Mssql Options",
                                                           "options for mssql connect.")
        self.subparsers = self.parser.add_subparsers(title="Mssql Actions",
                                                     description="Action mode for mssql.",
                                                     dest='option',
                                                     help="Specify your action for mssql.")
        self.mssql_parser.add_argument('-d', '--database',
                                       default='master',
                                       required=False,
                                       help='database name, default is %(default)s',
                                       dest='database')
        self.mssql_parser.add_argument('-t', '--timeout',
                                       default=30,
                                       type=int,
                                       required=False,
                                       help='query timeout, default is %(default)s',
                                       dest='timeout')
        self.mssql_parser.add_argument('-l', '--login_timeout',
                                       default=60,
                                       type=int,
                                       required=False,
                                       help='connection and login time out, default is %(default)s',
                                       dest='login_timeout')
        self.mssql_parser.add_argument('-c', '--charset',
                                       default='utf8',
                                       type=str,
                                       required=False,
                                       help='set the charset, default is %(default)s',
                                       dest='charset')
