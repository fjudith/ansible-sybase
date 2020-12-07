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
    import pyodbc as freetds_driver
except ImportError:
    PYODBC_IMP_ERR = traceback.format_exc()
    pyodbc_found = False
else:
    pyodbc_found = True

from ansible.module_utils.basic import AnsibleModule, missing_required_lib


def freetds_connect(module, login_user=None, login_password=None, server=None, port=None, driver=None,
                    connect_timeout=30, autocommit=False):
    
    # Connect to server
    db_connection = freetds_driver.connect(
        driver=driver,
        server=server,
        port=port,
        uid=login_user,
        pwd=login_password,
        connect_timeout=connect_timeout
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
