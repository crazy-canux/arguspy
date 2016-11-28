.. pymonitoringplugins documentation master file, created by
   sphinx-quickstart on Thu Nov  3 00:47:47 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==============================
Welcome to pymonitoringplugins
==============================

pymonitoringplugins is a pure python package for `[monitoring-plugins] <`[awesome-monitoring] <https://github.com/crazy-canux/awesome-monitoring>`_.

In this package you can use lots of protocols to get the monitoring data.

All you need to do is just focus on your monitoring business.

You don't need to pay attention on the basic protocols connection.

=======
Install
=======

Use pip::

    $pip install pymonitoringplugins

Use source code::

    $git clone https://github.com/crazy-canux/pymonitoringplugins.git
    $cd pymonitoringplugins
    $python setup.py install

===========
Quick Start
===========

Import the protocol you want::

    from pymonitoringplugins.http_requests import Http
    from pymonitoringplugins.ftp_ftplib import Ftp
    from pymonitoringplugins.ssh_paramiko import Ssh
    from pymonitoringplugins.mssql_pymssql import Mssql
    from pymonitoringplugins.mysql_pymysql import Mysql
    from pymonitoringplugins.winrm_pywinrm import WinRM
    from pymonitoringplugins.wmi_sh import Wmi
    from pymonitoringplugins.wmi_subprocess import Wmi

Write your own business monitoring class::

    class HttpSearch(Http):
        def __init__(self):
            super(HttpSearch, self).__init__()
            self.logger.debug("Init HttpSearch")

        def define_sub_options(self):
            super(HttpSearch, self).define_sub_options()
            self.hs_parser = self.subparsers.add_parser("...",
                                                        help='...',
                                                        description='...')
            self.hs_parser.add_argument('-s', '--search',
                                        default=None,
                                        required=False,
                                        help='Search pattern',
                                        dest='search')

        def httpsearch_handle(self):
            # Set the default status to ok.
            status = self.ok
            # Define your variables
            ...

            # Call the API to get the monitoring data.
            # Check the API from python/ipython console.
            # help(Http)
            # dir(Http)
            ...

            # Get the last status after check(Warning/Critical/Ok).
            ...

            # Set the output.
            self.shortoutput = "..."
            self.longoutput.append(...)
            self.perfdata.append(...)

            # Exit and show output.
            self.logger.debug("Return status and output.")
            status(self.output())

If put more than one business monitoring class in one plugin::

    class Register(HttpSearch, HttpCertificate):
        def __init__(self):
            super(Register, self).__init__()

Define main function::

    def main():
        # If just one class
        # plugin = HttpSearch()
        plugin = Register()
        arguments = sys.argv[1:]
        if 'httpsearch' in arguments:
            plugin.httpsearch_handle()
        else:
            plugin.unknown("Unknown Action.")

    if __name__ == "__main__":
        main()

==============
The User Guide
==============

.. toctree::
   :maxdepth: 2

   snmp
   http
   ftp
   ssh
   mysql
   mssql
   winrm
   wmi



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

