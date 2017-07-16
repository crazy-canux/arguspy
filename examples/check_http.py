#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test http/https with requests.

Copyright (C) 2016 Canux CHENG.
All rights reserved.
Name: test_http.py
Author: Canux CHENG canuxcheng@gmail.com
Version: V1.0.0
Time: Tue 08 Nov 2016 09:34:45 PM EST

DESCRIPTION:
    [1.2.0] 20170328 init for basic function.
"""
import sys

from arguspy.http_requests import Http


class HttpSearch(Http):

    """Check the URL reachable and search key words."""

    def __init__(self):
        super(HttpSearch, self).__init__()
        self.logger.debug("Init HttpSearch")

    def define_sub_options(self):
        super(HttpSearch, self).define_sub_options()
        self.hs_parser = self.subparsers.add_parser('httpsearch',
                                                    help='check url',
                                                    description='Options for url check.')
        self.hs_parser.add_argument('-s', '--search',
                                    default=None,
                                    required=False,
                                    help='Search pattern',
                                    dest='search')

    def httpsearch_handle(self):
        self.__content = self.connect().content
        self.close()
        self.logger.debug("content: {}".format(self.__content))

        status = self.ok

        if self.args.search in self.__content:
            status = self.ok
            self.shortoutput = "Http ok."
        else:
            status = self.critical
            self.shortoutput = "Http critical, can not find {}.".format(self.args.search)

        # Return status and output to monitoring server.
        self.logger.debug("Return status and output.")
        status(self.output())


class Register(HttpSearch):

    """Register your own class here."""

    def __init__(self):
        super(Register, self).__init__()


def test_http():
    plugin = Register()
    arguments = sys.argv[1:]
    if 'httpsearch' in arguments:
        plugin.httpsearch_handle()
    else:
        plugin.unknown("Unknown actions.")

if __name__ == "__main__":
    test_http()
