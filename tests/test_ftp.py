#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ftp plugins build with this library.

Copyright (C) 2017 Canux CHENG.
All rights reserved.
Name: check_ftp.py
Author: Canux CHENG canuxcheng@gmail.com
Version: V1.0.0
Time: Thu 28 Jul 2016 03:23:45 PM CST

Description:
"""

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import unittest

from arguspy.ftp_ftplib import Ftp

class TestFtp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_connect(self):
        ftp = Ftp()
        self.assertIsNotNone(ftp.connect(), msg='ftp connect failed.')

    def test_quit(self):
        pass

if __name__ == '__main__':
    unittest.main
