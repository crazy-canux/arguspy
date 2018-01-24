#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SUMMARY snmp_pysnmp.py

Copyright (C) 2017 Canux CHENG.
All rights reserved.

LICENSE GNU General Public License v3.0.

:author: Canux CHENG canuxcheng@gmail.com
:version: 0.0.1
:since: Thu 27 Jul 2017 10:15:38 AM EDT

DESCRIPTION:
"""
import pysnmp

from super_devops.monitoring.nagios_wrapper import BaseNagios


class Snmp(BaseNagios):

    "Wrapper pysnmp for monitoring plugins."

    def __init__(self):
        super(Snmp, self).__init__()
        self.logger.debug("Init snmp")
