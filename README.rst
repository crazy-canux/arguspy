
.. image:: https://img.shields.io/pypi/v/pymonitoringplugins.svg?maxAge=2592000
   :target: https://pypi.python.org/pypi/pymonitoringplugins/1.1.1.0

.. image:: https://coveralls.io/repos/github/crazy-canux/pymonitoringplugins/badge.svg?branch=master
    :target: https://coveralls.io/github/crazy-canux/pymonitoringplugins?branch=master

===================
pymonitoringplugins
===================

pymonitoringplugins is pure python code.

It's a API packge for monitoring plugins, like nagios or icinga.

`[awesome-monitoring] <https://github.com/crazy-canux/awesome-monitoring>`_.

--------------
How to install
--------------

Use pip to install:

    pip install pymonitoringplugins

----------
How to use
----------

Just import what protocol you need:

    from pymonitoringplugins.<protocol_package> import <Class>

    from pymonitoringplugins.ftp_ftplib import Ftp

    from pymonitoringplugins.mssql_pymssql import Mssql

    from pymonitoringplugins.mysql_pymysql import Mysql

    from pymonitoringplugins.ssh_paramiko import Ssh

    from pymonitoringplugins.winrm_pywinrm import WinRM

    from pymonitoringplugins.wmi_sh import Wmi

    from pymonitoringplugins.wmi_subprocess import Wmi

--------------
How to extends
--------------

Check the TODO list, you can give test examples or documents.

Also you can pull request for your code.

-----
TODO
-----

1. pymonitoringplugins/docs build with sphinx(2.0)
2. http(1.2)
3. snmp(1.3)
4. vmware-vsphere(1.4)

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
