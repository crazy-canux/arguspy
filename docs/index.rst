.. arguspy documentation master file, created by
   sphinx-quickstart on Thu Nov  3 00:47:47 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===================
arguspy
===================

arguspy is a pure python package for `[monitoring-plugins] <https://github.com/crazy-canux/awesome-monitoring>`_.

In this package you can use lots of protocols to get the monitoring data.

All you need to do is just focus on your monitoring business.

You don't need to pay attention on basic protocols connection and the basic functions about the monitoring tools.

=======
Install
=======

Use pip::

    $pip install arguspy

Use source code::

    $git clone https://github.com/crazy-canux/arguspy.git
    $cd arguspy
    $python setup.py install

===========
Quick Start
===========

Import the protocol you want::

    from arguspy.http_requests import Http
    from arguspy.ftp_ftplib import Ftp
    from arguspy.ssh_paramiko import Ssh
    from arguspy.mssql_pymssql import Mssql
    from arguspy.mysql_pymysql import Mysql
    from arguspy.winrm_pywinrm import WinRM
    from arguspy.wmi_sh import Wmi
    from arguspy.wmi_subprocess import Wmi
    ...

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

==========
How to use
==========

If you want to use this library and the plugins.

You must know something about the monitoring tools and protocols.

Output:

- $SERVICEOUTPUT$ -> ShortOutput
- $SERVICEPERFDATA$ -> PerfData
- $LONGSERVICEOUTPUT$ -> LongOutput

Return code:

- 0 OK
- 1 Warning
- 2 Critical
- 3 Unknown

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

