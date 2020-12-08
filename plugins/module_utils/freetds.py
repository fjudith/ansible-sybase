from __future__ import (absolute_import, division, print_function)
from functools import reduce
__metaclass__ = type

import os

from ansible.module_utils.six.moves import configparser
from ansible.module_utils._text import to_native

try:
    import pyodbc as freetds_driver
except ImportError:
    freeds_driver = None

freetds_driver_fail_msg = 'The PyODBC (Python 2.7 and Python 3.X) module is required.'

from ansible.module_utils.basic import AnsibleModule, missing_required_lib

def parse_from_odbcinst_config_file(odbcinst_file):
    # Default values of comment_prefix is '#' and ';'.
    # '!' added to prevent a parsing error
    # when a config file contains !includedir parameter.
    cp = configparser.ConfigParser(comment_prefixes=('#', ';', '!'))
    cp.read(odbcinst_file)
    
    return cp


def freetds_connect(module, odbc_driver='FreeTDS', login_user=None, login_password=None,
                    login_host=None, login_port=None, login_db=None,
                    connect_timeout=30, autocommit=False, encoding='utf-16le'):
    
    config = {}
    odbcinst_file = '/etc/odbcinst.ini'

    # if os.path.exists(odbcinst_file):
    #     try:
    #         cp_odbcinst = parse_from_odbcinst_config_file(odbcinst_file)
    #     except Exception as e:
    #         module.fail_json(msg="Failed to parse %s: %s" % (odbcinst_file, to_native(e)))

    # for key,value in cp_odbcinst['FreeTDS']:  
    #     print(key,value)

    config['host'] = login_host
    config['port'] = login_port

    # If login_user or login_password are given, they should override the
    # config file
    if odbc_driver is not None:
        config['driver'] = odbc_driver
    if login_user is not None:
        config['user'] = login_user
    if login_password is not None:
        config['password'] = login_password
    if login_db is not None:
        config['database'] = login_db
    if connect_timeout is not None:
        config['timeout'] = connect_timeout
    if encoding is not None:
        config['encoding'] = encoding
    if autocommit is not None:
        config['autocommit'] = autocommit

    print(config.items())

    db_connection = freetds_driver.connect(**config)

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

# Debug
if __name__ == '__main__':
    cursor, db_connection = freetds_connect(
        None, 'freetds', 'sa', 'myPassword', '127.0.0.1', 5000, 'master'
    )
    cursor.execute("SELECT @@version") 
    row = cursor.fetchone() 
    while row: 
        print(row[0])
        row = cursor.fetchone()