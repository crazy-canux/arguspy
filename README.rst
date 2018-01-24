.. image:: https://img.shields.io/pypi/v/arguspy.svg
   :target: https://pypi.python.org/pypi/arguspy/

.. image:: https://img.shields.io/pypi/dm/arguspy.svg
   :target: https://pypi.python.org/pypi/arguspy/

.. image:: https://travis-ci.org/crazy-canux/arguspy.svg?branch=master
   :target: https://travis-ci.org/crazy-canux/arguspy

.. image:: https://coveralls.io/repos/github/crazy-canux/arguspy/badge.svg?branch=master
   :target: https://coveralls.io/github/crazy-canux/arguspy?branch=master


=======
arguspy
=======

.. figure:: https://github.com/crazy-canux/arguspy/blob/master/data/images/argus.jpg
   :alt: pic1

[Deprecated] As nagios is too old, this project is deprecated.

Please Move to another project `[super-devops] <https://github.com/crazy-canux/super-devops>`_.

Arguspy is pure python code.

It's a API packge for monitoring plugins, like Nagios, Icinga, Naemon, Shinken, Centreon, Opsview and Sensu.

`[awesome-monitoring] <https://github.com/crazy-canux/awesome-monitoring>`_.

--------------
How to install
--------------

Use pip to install::

    $ pip install super_devops
    $ pip install arguspy

----------
How to use
----------

Just import what protocol you need::

    from arguspy.ftp_ftplib import Ftp
    from arguspy.http_requests import Http
    from arguspy.mssql_pymssql import Mssql
    from arguspy.mysql_pymysql import Mysql
    from arguspy.ssh_paramiko import Ssh
    from arguspy.winrm_pywinrm import WinRM
    from arguspy.wmi_sh import Wmi
    from arguspy.wmi_subprocess import Wmi

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
        plugin = Register()
        if plugin.args.option == 'action':
            plugin.action_handle()
        elif ...:
            ...
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

* Write unit tests in tests/
* Write docs in docs/
* Write examples in examples/

* Compatible with Python3
* vSphere monitoring
* LDAP monitoring
* SNMP monitoring

============
Contribution
============

`[Contribution] <https://github.com/crazy-canux/arguspy/blob/master/CONTRIBUTING.rst>`_

=======
Authors
=======

`[Authors] <https://github.com/crazy-canux/arguspy/blob/master/AUTHORS.rst>`_

=======
License
=======

`[License] <https://github.com/crazy-canux/arguspy/blob/master/LICENSE>`_
