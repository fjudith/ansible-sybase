from __future__ import (absolute_import, division, print_function)
from functools import reduce
__metaclass__ = type

import os
import traceback

from ansible.module_utils.six.moves import configparser
from ansible.module_utils._text import to_native

freetds_driver_fail_msg = 'The PyODBC (Python 2.7 and Python 3.X) module is required.'

PYODBC_IMP_ERR = None
try:
    import pymssql
except ImportError:
    PYMSSQL_IMP_ERR = traceback.format_exc()
    pyodbc_found = False
else:
    pyodbc_found = True

from ansible.module_utils.basic import AnsibleModule, missing_required_lib

def freetds_connect(module, login_user=None, login_password=None, server=None, port=None, driver=None, connect_timeout=30, autocommit=False):

    # If login_user or login_password are given, they should override the
    # config file
    if login_user is not None:
        config['user'] = login_user
    if login_password is not None:
        config['passwd'] = login_password
    if ssl_cert is not None:
        config['ssl']['cert'] = ssl_cert
    if ssl_key is not None:
        config['ssl']['key'] = ssl_key
    if ssl_ca is not None:
        config['ssl']['ca'] = ssl_ca
    if db is not None:
        config['db'] = db
    if connect_timeout is not None:
        config['connect_timeout'] = connect_timeout
    if check_hostname is not None:
        if mysql_driver.__name__ == "pyodbc":
            version_tuple = (n for n in mysql_driver.__version__.split('.') if n != 'None')
            if reduce(lambda x, y: int(x) * 100 + int(y), version_tuple) >= 711:
                config['ssl']['check_hostname'] = check_hostname
            else:
                module.fail_json(msg='To use check_hostname, pymysql >= 0.7.11 is required on the target host')

    db_connection = freetds_driver.connect(
        driver=driver,
        server=server,
        port=port,
        uid=login_user
        pwd=login_password
    )

    # Monkey patch the Connection class to close the connection when garbage collected
    def _conn_patch(conn_self):
        conn_self.close()
    db_connection.__class__.__del__ = _conn_patch
    # Patched

    return db_connection.cursor(), db_connection

def freetds_common_argument_spec():
    return dict(
        login_user=dict(type='str', default=None),
        login_password=dict(type='str', no_log=True),
        server=dict(type='str', default='localhost'),
        port=dict(type='int', default=5000),
        driver=dict(type='bool', default='FreeTDS'),
        connect_timeout=dict(type='int', default=30),
    )