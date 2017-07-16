#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ftp plugins build with this library.

Copyright (C) 2016 Canux CHENG.
All rights reserved.
Name: check_ftp.py
Author: Canux CHENG canuxcheng@gmail.com
Version: V1.0.0
Time: Thu 28 Jul 2016 03:23:45 PM CST

Description:
    [1.0.0] 20160728 init for basic function.

    example:
        ./check_ftp.py -H [IP] -u [USER] -p [PASSWORD] --debug filenumber -p "\\"
"""
import sys

from arguspy.ftp_ftplib import Ftp


class FileNumber(Ftp):

    """Count the file number in the ftp folder.

    TODO:
        -r
        -R
    """

    def __init__(self):
        super(FileNumber, self).__init__()
        self.logger.debug("Init FileNumber")

    def define_sub_options(self):
        super(FileNumber, self).define_sub_options()
        self.fn_parser = self.subparsers.add_parser('filenumber',
                                                    help='Count file number.',
                                                    description='Options\
                                                    for filenumber.')
        self.fn_parser.add_argument('-p', '--path',
                                    required=True,
                                    help='The folder you want to count.',
                                    dest='path')
        self.fn_parser.add_argument('-r', '--regex',
                                    required=False,
                                    help='RE for filename or extension',
                                    dest='regex')
        self.fn_parser.add_argument('-R', '--recursive',
                                    action='store_true',
                                    help='Recursive count file under path.',
                                    dest='recursive')
        self.fn_parser.add_argument('-w', '--warning',
                                    default=0,
                                    type=int,
                                    required=False,
                                    help='Warning value for filenumber, default is %(default)s',
                                    dest='warning')
        self.fn_parser.add_argument('-c', '--critical',
                                    default=0,
                                    type=int,
                                    required=False,
                                    help='Critical value for filenumber, default is %(default)s',
                                    dest='critical')

    def filenumber_handle(self):
        """Get the number of files in the folder."""
        self.__results = []
        self.__dirs = []
        self.__files = []
        self.__ftp = self.connect()
        self.__ftp.dir(self.args.path, self.__results.append)
        self.logger.debug("dir results: {}".format(self.__results))
        self.quit()

        status = self.ok

        for data in self.__results:
            if "<DIR>" in data:
                self.__dirs.append(str(data.split()[3]))
            else:
                self.__files.append(str(data.split()[2]))

        self.__result = len(self.__files)
        self.logger.debug("result: {}".format(self.__result))

        # Compare the vlaue.
        if self.__result > self.args.warning:
            status = self.warning
        if self.__result > self.args.critical:
            status = self.critical

        # Output
        self.shortoutput = "Found {0} files in {1}.".format(self.__result,
                                                            self.args.path)
        [self.longoutput.append(line) for line in self.__results if self.__results]
        self.perfdata.append("{path}={result};{warn};{crit};0;".format(
            crit=self.args.critical,
            warn=self.args.warning,
            result=self.__result,
            path=self.args.path))

        self.logger.debug("Return status and output.")
        status(self.output())


class Register(FileNumber):

    """Register your own class here."""

    def __init__(self):
        super(Register, self).__init__()


def main():
    """Register your own mode and handle method here."""
    plugin = Register()
    arguments = sys.argv[1:]
    if 'filenumber' in arguments:
        plugin.filenumber_handle()
    else:
        plugin.unknown("Unknown actions.")

if __name__ == "__main__":
    main()
