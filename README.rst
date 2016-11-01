.. image:: https://img.shields.io/pypi/v/nine.svg
   :target: https://pypi.python.org/pypi/pymonitoringplugins/1.1.0.0

.. image:: https://img.shields.io/pypi/dm/Django.svg
   :target: https://pypi.python.org/pypi/pymonitoringplugins/1.1.0.0

===================
pymonitoringplugins
===================

pymonitoringplugins is pure python code.

It's a API packge for monitoring plugins, like nagios or icinga.

`[awesome-monitoring] <https://github.com/crazy-canux/awesome-monitoring>`_.

--------------
How to install
--------------

Use pip to install::

    pip install pymonitoringplugins

----------
How to use
----------

Just import what protocol you need::

    from pymonitoringplugins.ftp_ftplib import Ftp
    from pymonitoringplugins.mssql_pymssql import Mssql
    from pymonitoringplugins.mysql_pymysql import Mysql
    from pymonitoringplugins.ssh_paramiko import Ssh
    from pymonitoringplugins.winrm_pywinrm import WinRM
    from pymonitoringplugins.wmi_sh import Wmi
    from pymonitoringplugins.wmi_subprocess import Wmi

Then write your own function monitoring class::

    class YourClass(Ftp/Mssql/Ssh/WinRM/Wmi/Http/Snmp/...):
        def __init__(self):
            super(YourClass, self).__init__()
            self.logger.debug("Init YourClass.")

        def define_sub_options(self):
            super(YourClass, self).define_sub_options()
            self.your_parser = self.subparsers.add_parser(...)
            self.your_parser.add_argument(...)
            ...

        def your_handle(self):
            """Put your function monitoring code here."""
            # Default status is ok.
            status = self.ok

            # Call the API and get the monitoring data.
            # Read the document or check the API on python/ipython Interactive console.
            # help(Ftp/...)
            # dir(Ftp/...)
            ...

            #  Compare with the warning and critical value and change the status.
            ...

            self.shortoutput = "..."
            self.longoutput.append(...)
            self.perfdata.append(...)

            self.logger.debug("Return status and output.")
            status(self.output())

If you put more than one function monitoring class in one file(Not recommend)::

    class Register(YourClass1, YourClass2, ...):
        def __init__(self):
            super(Register, self).__init__()

Last step::

    def main():
        # For multiple inherit
        # plugin = Register()
        plugin = YourClass()
        arguments = sys.argv[1:]
        if 'your' in arguments:
            plugin.your_handle()
        elif 'your2' in arguments:
            plugin.your2_handle()
        else:
            plugin.unknown("Unknown actions.")

    if __name__ == "__main__":
        main()

--------------
How to extends
--------------

Check the TODO list, you can give test examples or documents.

Also you can pull request for your code.

-----
TODO
-----

1. pymonitoringplugins/docs build with sphinx(2.0)
2. Thresholders need follow nagios rules(1.2)
3. http(1.3)
4. snmp(1.4)

============
Contribution
============

`[Contribution] <https://github.com/crazy-canux/pymonitoringplugins/blob/master/CONTRIBUTING.rst>`_

=======
Authors
=======

`[Authors] <https://github.com/crazy-canux/pymonitoringplugins/blob/master/AUTHORS.rst>`_

=======
License
=======

`[License] <https://github.com/crazy-canux/pymonitoringplugins/blob/master/LICENSE>`_
