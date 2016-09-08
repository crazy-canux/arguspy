#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Copyright (C) 2015 Faurecia (China) Holding Co.,Ltd.

All rights reserved.
Name: mysql_pymysql.py
Author: Canux CHENG canuxcheng@gmail.com
Version: V1.0.0.0
Time: Wed 27 Jul 2016 02:32:05 PM CST

Description:
    [1.0.0.0] 20160727 Init this plugin for basic functions.
"""
import pymysql

from monitor import Monitor


class Mysql(Monitor):

    """Basic class for mysql."""

    def __init__(self, *args, **kwargs):
        super(Mysql, self).__init__(*args, **kwargs)
        self.logger.debug("Init Mysql")
        try:
            self.conn = pymysql.connect(host=self.args.host,
                                        user=self.args.user,
                                        password=self.args.password,
                                        database=self.args.database,
                                        connect_timeout=self.args.login_timeout,
                                        charset=self.args.charset,
                                        cursorclass=self.args.as_dict)
            self.logger.debug("mysql connect succeed.")
        except pymysql.Error as e:
            self.unknown("Can not connect to the mysql: %s" % e)

    def query(self, sql_query):
        try:
            self.cursor = self.conn.cursor()
            self.logger.debug("get cursor ok")
        except pymysql.Error as e:
            self.unknown("Get cursor error: %s" % e)
        try:
            self.logger.debug("sql: {}".format("".join(sql_query)))
            self.cursor.execute("".join(sql_query))
            self.logger.debug("execute ok")
        except pymysql.Error as e:
            self.unknown("Execute sql error: %s" % e)
        try:
            self.results = self.cursor.fetchall()
            self.logger.debug("fetchall ok")
        except pymysql.Error as e:
            self.unknown("Fetchall error: %s" % e)
        try:
            self.cursor.close()
            self.logger.debug("Close cursor ok")
        except pymysql.Error as e:
            self.unknown("Close cursor error: %s" % e)
        return self.results

    def close(self):
        """Close the connection."""
        try:
            self.conn.close()
            self.logger.debug("Close connect succeed.")
        except pymysql.Error as e:
            self.unknown("Close connect error: %s" % e)

    def define_sub_options(self):
        super(Mysql, self).define_sub_options()
        self.mysql_parser = self.parser.add_argument_group("Mysql Options",
                                                           "options for mysql connect.")
        self.subparsers = self.parser.add_subparsers(title="Mysql Actions",
                                                     description="Action mode for mysql.",
                                                     help="Speficy you action for mysql.")
        self.mysql_parser.add_argument('-d', '--database',
                                       default='master',
                                       required=False,
                                       help='database name, default is %(default)s',
                                       dest='database')
        self.mysql_parser.add_argument('-l', '--login_timeout',
                                       default=60,
                                       type=int,
                                       required=False,
                                       help='connection and login time out, default is %(default)s',
                                       dest='login_timeout')
        self.mysql_parser.add_argument('-c', '--charset',
                                       default='utf8',
                                       type=str,
                                       required=False,
                                       help='set the charset, default is %(default)s',
                                       dest='charset')
        self.mysql_parser.add_argument('--as_dict',
                                       default=pymysql.cursors.SSCursor,
                                       required=False,
                                       help='Set the return mode, SSCursro is tupple, DictCursor is dict.',
                                       dest='as_dict')