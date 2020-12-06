from __future__ import (absolute_import, division, print_function)
from functools import reduce

__metaclass__ = type

import os
import traceback

from ansible.module_utils.six.moves import configparser
from ansible.module_utils._text import to_native

freetds_driver_fail_msg = 'The PyODBC (Python 2.7 and Python 3.X) module is required.'

try:
    import pyodbc as freetds_driver
except ImportError:
    try:
        import pymssql as freetds_driver
    except ImportError:
        freetds_driver = None

from ansible.module_utils.basic import AnsibleModule, missing_required_lib


def freetds_connect(module, login_user=None, login_password=None,
                    login_host=None, login_port=None, db=None,
                    connect_timeout=30, autocommit=False, encoding='utf-16le', odbc_driver='FreeTDS'):
    
    connection_string = {}

    connection_string['server'] = login_host
    connection_string['port'] = login_port
    
    # If login_user or login_password are given, they should override the
    # config file
    if odbc_driver is not None:
        connection_string['driver'] = odbc_driver
    if login_user is not None:
        connection_string['uid'] = login_user
    if login_password is not None:
        connection_string['pwd'] = login_password
    if db is not None:
        connection_string['database'] = db
    if connect_timeout is not None:
        connection_string['timeout'] = connect_timeout
    if encoding is not None:
        connection_string['encoding'] = encoding
    
    # Connect to server
    db_connection = freetds_driver.connect(autocommit=autocommit, **connection_string)

    # Monkey patch the Connection class to close the connection when garbage collected
    def _conn_patch(conn_self):
        conn_self.close()
    db_connection.__class__.__del__ = _conn_patch
    # Patched

    return db_connection.cursor(), db_connection

# ref: https://github.com/mkleehammer/pyodbc/wiki/The-pyodbc-Module#connect
def freetds_common_argument_spec():
    return dict(
        login_user=dict(type='str', default=None),
        login_password=dict(type='str', no_log=True),
        login_host=dict(type='str', default='localhost'),
        login_port=dict(type='int', default=5000),
        odbc_driver=dict(type='str', default='FreeTDS'),
        connect_timeout=dict(type='int', default=30),
        encoding=dict(type='str', default='utf-16le'),
    )
