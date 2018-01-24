#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Basic function for http/https build with third party library requests.

Copyright (C) 2016 Canux CHENG.
All rights reserved.
Name: http_requests.py
Author: Canux CHENG canuxcheng@gmail.com
Version: V1.0.0
Time: Tue 13 Sep 2016 02:12:28 AM EDT

DESCRIPTION:
    [1.2.0] 20170328 init for basic function.
"""
import requests

from super_devops.monitoring.nagios_wrapper import BaseNagios


class Http(BaseNagios):

    """Basic class for http/https."""

    def __init__(self):
        super(Http, self).__init__()
        self.logger.debug("Init Http.")

        try:
            self.auth = None if not self.args.user else (self.args.user, self.args.password)
            self.protocol = 'http' if not self.args.ssl else 'https'
            self.url = '{0}://{1}:{2}{3}'.format(self.protocol,
                                                 self.args.host,
                                                 self.args.port,
                                                 self.args.path)
            self.response = requests.request(self.args.method,
                                             url=self.url, auth=self.auth,
                                             allow_redirects=self.args.allow_redirects,
                                             verify=self.args.verify,
                                             stream=self.args.stream,
                                             timeout=self.args.timeout,
                                             cert=self.args.cert,
                                             params=self.args.params,
                                             data=self.args.data,
                                             json=self.args.json,
                                             headers=self.args.headers,
                                             cookies=self.args.cookies,
                                             files=self.args.files,
                                             proxies=self.args.proxies)
            if self.response.status_code != 200:
                self.unknown("Connect {0} error: {1}".format(
                    self.url, self.response.status_code))
            self.logger.debug("{} connect succeed.".format(self.url))
        except Exception as e:
            self.unknown("{0} {1} error: {2}".format(self.args.method, self.url, e))

    def connect(self):
        """Connect to http/https server."""
        return self.response

    def close(self):
        """Close the http/https connect."""
        try:
            self.response.close()
            self.logger.debug("close connect succeed.")
        except Exception as e:
            self.unknown("close connect error: %s" % e)

    def define_sub_options(self):
        super(Http, self).define_sub_options()
        self.http_parser = self.parser.add_argument_group("Http options",
                                                          "options for http/https")
        self.subparsers = self.parser.add_subparsers(title="Http/Https actions",
                                                     description="Action mode for http/https",
                                                     dest='option',
                                                     help="Specify your action for http/https.")
        self.http_parser.add_argument('-S', '--ssl',
                                      action='store_true',
                                      default=False,
                                      help='Default without ssl and use http, -S to specify use ssl.',
                                      dest='ssl')
        self.http_parser.add_argument('-P', '--port',
                                      default=80,
                                      type=int,
                                      required=False,
                                      help='Default is %(default)s.',
                                      dest='port')
        self.http_parser.add_argument('-d', '--path',
                                      default='/',
                                      required=False,
                                      help='Default is %(default)s.',
                                      dest='path')
        self.http_parser.add_argument('-m', '--method',
                                      default='get',
                                      required=False,
                                      help='Default is %(default)s.',
                                      dest='method')
        self.http_parser.add_argument('-a', '--allow_redirects',
                                      action='store_true',
                                      default=True,
                                      help='Default is %(default)s if POST/PUT/DELETE redirect following is allowed.',
                                      dest='allow_redirects')
        self.http_parser.add_argument('-v', '--verify',
                                      action='store_true',
                                      default=True,
                                      help='Default is %(default)s if the SSL cert will be verified.',
                                      dest='verify')
        self.http_parser.add_argument('-s', '--stream',
                                      action='store_true',
                                      default=True,
                                      help='Default is %(default)s if the response content will not be immediately downloaded.',
                                      dest='stream')
        self.http_parser.add_argument('-t', '--timeout',
                                      default=(10, 10),
                                      type=tuple,
                                      required=False,
                                      help='Default is %(default)s. For connect timeout and read timeout',
                                      dest='timeout')
        self.http_parser.add_argument('-c', '--cert',
                                      default=None,
                                      type=tuple,
                                      required=False,
                                      help='Defauit is %(default)s. For cert pem file and key pem file.',
                                      dest='cert')
        self.http_parser.add_argument('--params',
                                      default=None,
                                      type=dict,
                                      required=False,
                                      help='Default is %(default)s.',
                                      dest='params')
        self.http_parser.add_argument('--headers',
                                      default=None,
                                      type=dict,
                                      required=False,
                                      help='Default is %(default)s.',
                                      dest='headers')
        self.http_parser.add_argument('--json',
                                      default=None,
                                      required=False,
                                      help='Default is %(default)s. Json data to send in the body.',
                                      dest='json')
        self.http_parser.add_argument('--data',
                                      default=None,
                                      type=dict,
                                      required=False,
                                      help='Default is %(default)s.',
                                      dest='data')
        self.http_parser.add_argument('--files',
                                      default=None,
                                      type=dict,
                                      required=False,
                                      help='Default is %(default)s.',
                                      dest='files')
        self.http_parser.add_argument('--cookies',
                                      default=None,
                                      type=dict,
                                      required=False,
                                      help='Default is %(default)s.',
                                      dest='cookies')
        self.http_parser.add_argument('--proxies',
                                      default=None,
                                      type=dict,
                                      required=False,
                                      help='Default is %(default)s.',
                                      dest='proxies')
