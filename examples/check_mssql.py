#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Mssql plugins build with this library.

Copyright (C) 2016 Canux CHENG.
All rights reserved.
Name: check_mssql.py
Author: Canux CHENG canuxcheng@gmail.com
Version: V1.0.0
Time: Wed 27 Jul 2016 02:01:20 PM CST

Description:
    [1.0.0] 20160727 Init this plugin for basic functions.
"""
import sys
import re

from arguspy.mssql_pymssql import Mssql


class Sql(Mssql):

    """Just for the return value is a single number."""

    def __init__(self):
        super(Sql, self).__init__()
        self.logger.debug("Init Sql")

    def define_sub_options(self):
        super(Sql, self).define_sub_options()
        self.sql_parser = self.subparsers.add_parser('sql',
                                                     help='Run sql/SP.',
                                                     description='Options\
                                                     for sql/SP.')
        self.sql_parser.add_argument('-s', '--sql',
                                     action='append',
                                     type=str,
                                     required=True,
                                     help='The sql or store procedure.',
                                     dest='sql')
        self.sql_parser.add_argument('-w', '--warning',
                                     default=0,
                                     type=int,
                                     required=False,
                                     help='Warning value for sql, default is %(default)s',
                                     dest='warning')
        self.sql_parser.add_argument('-c', '--critical',
                                     default=0,
                                     type=int,
                                     required=False,
                                     help='Critical value for sql, default is %(default)s',
                                     dest='critical')
        self.sql_parser.add_argument('--as_dict',
                                     default=False,
                                     type=bool,
                                     required=False,
                                     help='Set the return mode.',
                                     dest='as_dict')

    def sql_handle(self):
        self.__results = self.query(self.args.sql)
        self.close()
        self.logger.debug("results: {}".format(self.__results))
        if not self.__results:
            self.unknown("SP/SQL return nothing.")
        if len(self.__results) != 1:
            self.unknown("SP/SQL return more than one number.")
        self.__result = self.__results[0][0]
        if not isinstance(self.__result, (int, long)):
            self.unknown("SP/SQL not return a single number.")
        self.logger.debug("result: {}".format(self.__result))
        status = self.ok

        # Compare the vlaue.
        if self.__result > self.args.warning:
            status = self.warning
        if self.__result > self.args.critical:
            status = self.critical

        # Output
        self.shortoutput = "The result is {}".format(self.__result)
        self.longoutput.append("-------------------------------\n")
        self.longoutput.append(str(self.__results))
        self.longoutput.append("-------------------------------\n")
        self.perfdata.append("\n{sql}={result};{warn};{crit};0;".format(
            crit=self.args.critical,
            warn=self.args.warning,
            result=self.__result,
            sql=self.args.sql))

        # Return status with message to Nagios.
        self.logger.debug("Return status and output.")
        status(self.output())


class DatabaseUsed(Mssql):

    """For check the database-size, database-used, database-percent."""

    def __init__(self):
        super(DatabaseUsed, self).__init__()
        self.logger.debug("Init databaseused")

    def define_sub_options(self):
        super(DatabaseUsed, self).define_sub_options()
        self.du_parser = self.subparsers.add_parser('database-used',
                                                    help='For\
                                                    database-used.',
                                                    description='Options\
                                                    for database-used.')
        self.du_parser.add_argument('-w', '--warning',
                                    default=0,
                                    type=int,
                                    required=False,
                                    help='Warning value for data file, default is %(default)s',
                                    dest='warning')
        self.du_parser.add_argument('-c', '--critical',
                                    default=0,
                                    type=int,
                                    required=False,
                                    help='Critical value for data file, default is %(default)s',
                                    dest='critical')
        self.du_parser.add_argument('-r', '--regex',
                                    required=False,
                                    help='Specify the DB you want.',
                                    dest='regex')
        self.du_parser.add_argument('--as_dict',
                                    default=True,
                                    type=bool,
                                    required=False,
                                    help='Set the return mode.',
                                    dest='as_dict')

    def database_used_handle(self):
        self.database_used_sql = """
SET  NOCOUNT ON;
SET  ANSI_NULLS ON;
SET  QUOTED_IDENTIFIER ON;

DECLARE
  @SQL     NVARCHAR(4000),
  @dbname  sysname;

declare
  @datatab table
          (name    sysname,
           dbsize  float,
           dbused  float,
           logsize float,
           logused float);

declare
  dbcursor      cursor for
                select name from sys.databases order by database_id;

open dbcursor;
fetch NEXT FROM dbcursor INTO @dbname;

while @@FETCH_STATUS = 0
BEGIN
  set @SQL='use ' + quotename(@dbname) + '; SELECT ''' +  @dbname + ''' as dbname' +
       ', (SELECT SUM(CAST(size AS FLOAT)) / 128 FROM sys.database_files WHERE  type IN (0, 2, 4)) dbsize' +
       ', SUM(CAST(a.total_pages AS FLOAT)) / 128 reservedsize' +
       ', (SELECT SUM(CAST(size AS FLOAT)) / 128 FROM sys.database_files WHERE  type IN (1, 3)) logsize' +
       ', (select sum(cast(fileproperty(name, ''SpaceUsed'') as float))/128 from sys.database_files where type in (1,3)) logUsedMB' +
       ' FROM ' + quotename(@dbname) + '.sys.partitions p' +
       ' INNER JOIN ' + quotename(@dbname) + '.sys.allocation_units a ON p.partition_id = a.container_id' +
       ' LEFT OUTER JOIN ' + quotename(@dbname) + '.sys.internal_tables it ON p.object_id = it.object_id';

  insert into @datatab
  execute(@SQL);
  --print @SQL
  fetch NEXT FROM dbcursor INTO @dbname;
end;

CLOSE dbcursor;
DEALLOCATE dbcursor;

select  name
      , dbsize
      , dbused
      , round(dbused / dbsize *100, 2) dbpercent
from @datatab d order by name;
"""
        self.__dbwarn = []
        self.__dbwarn_rest = []
        self.__dbcrit = []
        self.__dbcrit_rest = []
        self.__new_results = []

        self.__results = self.query(self.database_used_sql)
        self.close()
        self.logger.debug("results: {}".format(self.__results))

        # filter.
        if self.args.regex:
            for loop in range(0, len(self.__results)):
                self.logger.debug("line_dict {0}: {1}".format(
                    loop, self.__results[loop]))
                name = str(self.__results[loop]['name'])
                if re.findall(self.args.regex, name):
                    self.__new_results.append(self.__results[loop])
        else:
            self.__new_results = self.__results

        status = self.ok
        self.__result = []
        self.__result_rest = self.__new_results

        for loop in range(0, len(self.__new_results)):
            line_dict = self.__new_results[loop]
            dbsize = float(line_dict['dbsize'])

            # Compare the db
            if self.args.warning:
                if dbsize > self.args.warning:
                    self.__dbwarn.append(line_dict)
                else:
                    self.__dbwarn_rest.append(line_dict)
            if self.args.critical:
                if dbsize > self.args.critical:
                    self.__dbcrit.append(line_dict)
                else:
                    self.__dbcrit_rest.append(line_dict)

        # get status and results.
        if len(self.__dbwarn):
            status = self.warning
            self.__result = self.__dbwarn
            self.__result_rest = self.__dbwarn_rest
        if len(self.__dbcrit):
            status = self.critical
            self.__result = self.__dbcrit
            self.__result_rest = self.__dbcrit_rest

        # Output for nagios
        self.shortoutput = "{0} db, {1} db warning, {2} db critical.".format(
            len(self.__new_results), len(self.__dbwarn), len(self.__dbcrit))
        self.longoutput.append("---------------------------------\n")
        self.__write_longoutput(self.__result)
        self.longoutput.append("=============== OK ===============\n")
        self.__write_longoutput(self.__result_rest)
        self.perfdata.append("\nError number={result};{warn};{crit};0;".format(
            crit=self.args.critical,
            warn=self.args.warning,
            result=len(self.__result)))

        # Return status with message to Nagios.
        self.logger.debug("Return status and output.")
        status(self.output())

    def __write_longoutput(self, result):
        try:
            if result:
                if isinstance(result[0], dict):
                    keys = result[0].keys()
                    for loop in range(0, len(result)):
                        for key in keys:
                            value = str(result[loop].get(key)).strip("\n")
                            if key == 'dbpercent':
                                unit = "%"
                            elif key == 'dbsize':
                                unit = "MB"
                            elif key == 'dbused':
                                unit = "MB"
                            else:
                                unit = ""
                            line = key + ": " + value + unit
                            self.longoutput.append(line + "\n")
                        self.longoutput.append("---------------------------\n")
        except Exception as e:
            self.unknown("database-used write_longoutput error: {}".format(e))


class DatabaseLogUsed(Mssql):

    """For check database-log-size, database-log-used, database-log-percent."""

    def __init__(self):
        super(DatabaseLogUsed, self).__init__()
        self.logger.debug("Init databaselogused")

    def define_sub_options(self):
        super(DatabaseLogUsed, self).define_sub_options()
        self.dl_parser = self.subparsers.add_parser('databaselog-used',
                                                    help='For\
                                                    databaselog-used.',
                                                    description='Options\
                                                    for databaselog-used.')
        self.dl_parser.add_argument('-w', '--warning',
                                    default=0,
                                    type=int,
                                    required=False,
                                    help='Warning value for log file, default is %(default)s',
                                    dest='warning')
        self.dl_parser.add_argument('-c', '--critical',
                                    default=0,
                                    type=int,
                                    required=False,
                                    help='Critical value for log file, default is %(default)s',
                                    dest='critical')
        self.dl_parser.add_argument('-r', '--regex',
                                    required=False,
                                    help='Specify the DB you want.',
                                    dest='regex')
        self.dl_parser.add_argument('--as_dict',
                                    default=True,
                                    type=bool,
                                    required=False,
                                    help='Set the return mode.',
                                    dest='as_dict')

    def database_log_used_handle(self):
        self.databaselog_used_sql = """
SET  NOCOUNT ON;
SET  ANSI_NULLS ON;
SET  QUOTED_IDENTIFIER ON;

DECLARE
  @SQL     NVARCHAR(4000),
  @dbname  sysname;

declare
  @datatab table
          (name    sysname,
           dbsize  float,
           dbused  float,
           logsize float,
           logused float);

declare
  dbcursor      cursor for
                select name from sys.databases order by database_id;

open dbcursor;
fetch NEXT FROM dbcursor INTO @dbname;

while @@FETCH_STATUS = 0
BEGIN
  set @SQL='use ' + quotename(@dbname) + '; SELECT ''' +  @dbname + ''' as dbname' +
       ', (SELECT SUM(CAST(size AS FLOAT)) / 128 FROM sys.database_files WHERE  type IN (0, 2, 4)) dbsize' +
       ', SUM(CAST(a.total_pages AS FLOAT)) / 128 reservedsize' +
       ', (SELECT SUM(CAST(size AS FLOAT)) / 128 FROM sys.database_files WHERE  type IN (1, 3)) logsize' +
       ', (select sum(cast(fileproperty(name, ''SpaceUsed'') as float))/128 from sys.database_files where type in (1,3)) logUsedMB' +
       ' FROM ' + quotename(@dbname) + '.sys.partitions p' +
       ' INNER JOIN ' + quotename(@dbname) + '.sys.allocation_units a ON p.partition_id = a.container_id' +
       ' LEFT OUTER JOIN ' + quotename(@dbname) + '.sys.internal_tables it ON p.object_id = it.object_id';

  insert into @datatab
  execute(@SQL);
  --print @SQL
  fetch NEXT FROM dbcursor INTO @dbname;
end;

CLOSE dbcursor;
DEALLOCATE dbcursor;

select  name
      , logsize
      , logused
      ,round(logused / logsize *100, 2) logpercent
from @datatab d order by name;
"""
        self.__logwarn = []
        self.__logwarn_rest = []
        self.__logcrit = []
        self.__logcrit_rest = []
        self.__new_results = []

        self.__results = self.query(self.databaselog_used_sql)
        self.close()
        self.logger.debug("results: {}".format(self.__results))

        # filter
        if self.args.regex:
            for loop in range(0, len(self.__results)):
                self.logger.debug("line_dict {0}: {1}".format(
                    loop, self.__results[loop]))
                name = str(self.__results[loop]['name'])
                if re.findall(self.args.regex, name):
                    self.__new_results.append(self.__results[loop])
        else:
            self.__new_results = self.__results

        status = self.ok
        self.__result = []
        self.__result_rest = self.__new_results

        for loop in range(0, len(self.__new_results)):
            line_dict = self.__new_results[loop]
            logsize = float(line_dict['logsize'])

            # Compare the db
            if self.args.warning:
                if logsize > self.args.warning:
                    self.__logwarn.append(line_dict)
                else:
                    self.__logwarn_rest.append(line_dict)
            if self.args.critical:
                if logsize > self.args.critical:
                    self.__logcrit.append(line_dict)
                else:
                    self.__logwarn_rest.append(line_dict)

        # get status and result.
        if len(self.__logwarn):
            status = self.warning
            self.__result = self.__logwarn
            self.__result_rest = self.__logwarn_rest
        if len(self.__logcrit):
            status = self.critical
            self.__result = self.__logcrit
            self.__result_rest = self.__logcrit_rest

        # Output for nagios
        self.shortoutput = "{0} dblog, {1} warning, {2} critical.".format(
            len(self.__new_results), len(self.__logwarn), len(self.__logcrit))
        self.longoutput.append("---------------------------------\n")
        self.__write_longoutput(self.__result)
        self.longoutput.append("=============== OK ===============\n")
        self.__write_longoutput(self.__result_rest)
        self.perfdata.append("\nError number={result};{warn};{crit};0;".format(
            crit=self.args.critical,
            warn=self.args.warning,
            result=len(self.__result)))

        # Return status with message to Nagios.
        self.logger.debug("Return status and output.")
        status(self.output())

    def __write_longoutput(self, result):
        try:
            if result:
                if isinstance(result[0], dict):
                    keys = result[0].keys()
                    for loop in range(0, len(result)):
                        for key in keys:
                            value = str(result[loop].get(key)).strip("\n")
                            if key == 'logpercent':
                                unit = "%"
                            elif key == 'logsize':
                                unit = "MB"
                            elif key == 'logused':
                                unit = "MB"
                            else:
                                unit = ""
                            line = key + ": " + value + unit
                            self.longoutput.append(line + "\n")
                        self.longoutput.append("---------------------------\n")
        except Exception as e:
            self.unknown("databaselog-used write_longoutput error: {}".format(
                e))


class Register(Sql, DatabaseUsed, DatabaseLogUsed):

    """Register your own class here."""

    def __init__(self):
        super(Register, self).__init__()


def main():
    """Register your own mode and handle method here."""
    plugin = Register()
    arguments = sys.argv[1:]
    if 'sql' in arguments:
        plugin.sql_handle()
    elif 'database-used' in arguments:
        plugin.database_used_handle()
    elif 'databaselog-used' in arguments:
        plugin.database_log_used_handle()
    else:
        plugin.unknown("Unknown actions.")

if __name__ == "__main__":
    main()
