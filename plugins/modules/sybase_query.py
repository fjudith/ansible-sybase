  
#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: sybase_query
short_description: Run Sybase queries
description:
- Runs arbitrary Sybase queries.
- Pay attention, the module does not support check mode!
  All queries will be executed in autocommit mode.
- To run SQL queries from a file, use M(sqlops.sybase.sybase_db) module.
version_added: '0.1.0'
options:
  query:
    description:
    - SQL query to run. Multiple queries can be passed using YAML list syntax.
    - Must be a string or YAML list containing strings.
    type: raw
    required: yes
  positional_args:
    description:
    - List of values to be passed as positional arguments to the query.
    - Mutually exclusive with I(named_args).
    type: list
  named_args:
    description:
    - Dictionary of key-value arguments to pass to the query.
    - Mutually exclusive with I(positional_args).
    type: dict
  login_db:
    description:
    - Name of database to connect to and run queries against.
    type: str
  single_transaction:
    description:
    - Where passed queries run in a single transaction (C(yes)) or commit them one-by-one (C(no)).
    type: bool
    default: no
seealso:
- module: sqlops.sybase.sybase_db
author:
- Florian JUDITH (@fjudith)
extends_documentation_fragment:
- sqlops.sybase.sybase
'''

EXAMPLES = r'''
- name: Simple select query to acme db
  sqlops.sybase.sybase_query:
    login_db: acme
    query: SELECT * FROM orders
- name: Select query to db acme with positional arguments
  sqlops.sybase.sybase_query:
    login_db: acme
    query: SELECT * FROM acme WHERE id = %s AND story = %s
    positional_args:
    - 1
    - test
- name: Select query to test_db with named_args
  sqlops.sybase.sybase_query:
    login_db: test_db
    query: SELECT * FROM test WHERE id = %(id_val)s AND story = %(story_val)s
    named_args:
      id_val: 1
      story_val: test
- name: Run several insert queries against db test_db in single transaction
  sqlops.sybase.sybase_query:
    login_db: test_db
    query:
    - INSERT INTO articles (id, story) VALUES (2, 'my_long_story')
    - INSERT INTO prices (id, price) VALUES (123, '100.00')
    single_transaction: yes
'''

RETURN = r'''
results:
    description: List of lists of strings containing selected rows, likely empty for DDL statements.
    returned: success
    type: list
    elements: list
description:
    description: "List of dicts about the columns selected from the cursors, likely empty for DDL statements. See notes."
    returned: success
    type: list
    elements: dict
row_count:
    description: "The number of rows selected or modified according to the cursor defaults to -1. See notes."
    returned: success
    type: str
'''

import os

from ansible.module_utils.six.moves import configparser
from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible.module_utils._text import to_native

DML_QUERY_KEYWORDS = ('INSERT', 'UPDATE', 'DELETE')
# TRUNCATE is not DDL query but it also returns 0 rows affected:
DDL_QUERY_KEYWORDS = ('CREATE', 'DROP', 'ALTER', 'RENAME', 'TRUNCATE')

DQL_QUERY_KEYWORDS = ('SELECT')

DCL_QUERY_KEYWORDS = ('GRANT', 'REVOKE')

# Import ODBC drivers
try:
    import pyodbc as sybase_driver
except ImportError:
    try:
        import pymssql as sybase_driver
    except ImportError:
        sybese_driver = None

sybase_driver_fail_msg = 'The PyODBC (Python 2.7 and Python 3.X) module is required.'


# ===============================================
# Ansible support arguments.
# ref: https://github.com/mkleehammer/pyodbc/wiki/The-pyodbc-Module
# ===============================================
def sybase_common_argument_spec():
    return dict(
        login_user=dict(type='str', default=None),
        login_password=dict(type='str', no_log=True),
        login_host=dict(type='str', default='localhost'),
        login_port=dict(type='int', default=5000),
        odbc_driver=dict(type='str', default='FreeTDS'),
        connect_timeout=dict(type='int', default=30),
        encoding=dict(type='str', default='utf-16le'),
        query=dict(type='raw', required=True),
        login_db=dict(type='str'),
        positional_args=dict(type='list'),
        named_args=dict(type='dict'),
        single_transaction=dict(type='bool', default=False),
    )

# ===============================================
# Module execution.
# ===============================================
def main():
    # Prepare parameters
    argument_spec = sybase_common_argument_spec()
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=(
            ('positionnal_args', 'named_args'), 
        ),
    )

    # Mandatory parameters
    odbc_driver     = module.params['odbc_driver']
    login_host      = module.params['login_host']
    login_port      = module.params['login_port']
    login_user      = module.params['login_user']
    login_password  = module.params['login_password']
    login_db        = module.params['login_db']
    connect_timeout = module.params['connect_timeout']
    encoding        = module.params["encoding"]
    query           = module.params["query"]

    # Check query format
    if not isinstance(query, (str, list)):
        module.fail_json(msg="the query option value must be a string or list, passed %s" % type(query))

    # Convert query to string
    if isinstance(query, str):
        query = [query]

    # Change query array elements
    for elem in query:
        if not isinstance(elem, str):
            module.fail_json(msg="the elements in query list must be strings, passed '%s' %s" % (elem, type(elem)))
    
    # Disable autocommit when single transaction is enabled
    if module.params["single_transaction"]:
        autocommit = False
    else:
        autocommit = True
    
    # Prepare args:
    if module.params.get("positional_args"):
        arguments = module.params["positional_args"]
    elif module.params.get("named_args"):
        arguments = module.params["named_args"]
    else:
        arguments = None  
    
    # Check ODBC driver initialization
    if sybase_driver is None:
        module.fail_json(msg=sybase_driver_fail_msg)
    
    # Connect to Database:
    try:
        db_connection = sybase_driver.connect(driver=odbc_driver, user=login_user, password=login_password,
                                              host=login_host, port=login_port, database=login_db,
                                              connect_timeout=connect_timeout, encoding=encoding,
                                              autocommit=autocommit)
    except Exception as e:
        module.fail_json(msg="unable to connect to database: '%s', check login_user and "
                             "login_password are correct."
                             "ODBC driver: '%s'. Exception message: '%s'" % (login_db, odbc_driver, to_native(e)))

    # Get cursor
    cursor = db_connection.cursor()

    max_keyword_len = len(max(DML_QUERY_KEYWORDS + DDL_QUERY_KEYWORDS, key=len))

    # Execute query:
    # Set defaults:
    result = dict(
        changed=False,
        description=[],
        row_count=-1,
        results=[],
    )

    for q in query:
        try:
            if arguments:
                cursor.execute(q, arguments)
            else:
                cursor.execute(q)

        except Exception as e:
            if not autocommit:
                db_connection.rollback()

            cursor.close()
            module.fail_json(msg="Cannot execute SQL '%s' args [%s]: %s" % (q, arguments, to_native(e)))

        try:
            # Get the rows out into an 2d array
            for row in cursor.fetchall():
                new_row = []
                for column in row:
                    new_row.append("{0}".format(column))
                result['results'].append(new_row)
            
            for row_description in cursor.description:
                description = {}
                description['name'] = row_description[0]
                description['type'] = row_description[1].__name__
                description['display_size'] = row_description[2]
                description['internal_size'] = row_description[3]
                description['precision'] = row_description[4]
                description['scale'] = row_description[5]
                description['nullable'] = row_description[6]

        except sybase_driver.ProgrammingError as pe:
            pass
        except Exception as e:
            if not autocommit:
                db_connection.rollback()

            module.fail_json(msg="Cannot fetch rows from cursor: %s" % to_native(e))

        # Check DML or DDL keywords in query and set changed accordingly:
        q = q.lstrip()[0:max_keyword_len].upper()
        for keyword in DML_QUERY_KEYWORDS:
            if keyword in q and cursor.rowcount > 0:
                result['changed'] = True

        for keyword in DDL_QUERY_KEYWORDS:
            if keyword in q:
                result['changed'] = True
        
        for keywork in DQL_QUERY_KEYWORDS:
            if keywork in q:
                result['changed'] = True

        # Get number of rows
        result['row_count'] = cursor.rowcount

    # When the module run with the single_transaction == True:
    if not autocommit:
        db_connection.commit()

    # Exit:
    module.exit_json(**result)


if __name__ == '__main__':
    main()