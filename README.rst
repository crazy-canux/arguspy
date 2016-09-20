
[![Coverage Status](https://coveralls.io/repos/github/crazy-canux/pyMonitoringPlugins/badge.svg?branch=master)](https://coveralls.io/github/crazy-canux/pyMonitoringPlugins?branch=master)

===================
pyMonitoringPlugins
===================

pyMonitoringPlugins is pure python code.

It's a API packge for monitoring plugins, like nagios or icinga.

`[awesome-monitoring] <https://github.com/crazy-canux/awesome-monitoring>`_.

--------------
How to install
--------------

Use pip to install:

    pip install pyMonitoringPlugins

----------
How to use
----------

Just import what protocol you need:

    from pyMonitoringPlugins.<protocol_package> import <Class>

    from pyMonitoringPlugins.ftp_ftplib import Ftp

    from pyMonitoringPlugins.mssql_pymssql import Mssql

    from pyMonitoringPlugins.mysql_pymysql import Mysql

    from pyMonitoringPlugins.ssh_paramiko import Ssh

    from pyMonitoringPlugins.winrm_pywinrm import WinRM

    from pyMonitoringPlugins.wmi_sh import Wmi

    from pyMonitoringPlugins.wmi_subprocess import Wmi

--------------
How to extends
--------------

Check the TODO list, you can give test examples or documents.

Also you can pull request for your code.

-----
TODO
-----

1. pyMonitoringPlugins/docs build with sphinx(2.0)
2. http(1.2)
3. snmp(1.3)
4. vmware-vsphere(1.4)

============
Contribution
============

`[Contribution] <https://github.com/crazy-canux/pyMonitoringPlugins/blob/master/CONTRIBUTING.rst>`_

=======
Authors
=======

`[Authors] <https://github.com/crazy-canux/pyMonitoringPlugins/blob/master/AUTHORS.rst>`_

=======
License
=======

`[License] <https://github.com/crazy-canux/pyMonitoringPlugins/blob/master/LICENSE>`_
