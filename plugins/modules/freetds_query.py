  
#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: freetds_query
short_description: Run FreeTDS queries
description:
- Runs arbitrary FreeTDS queries.
- Pay attention, the module does not support check mode!
  All queries will be executed in autocommit mode.
- To run SQL queries from a file, use M(community.sybase.sybase_db) module.
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
- module: community.sybase.sybase_db
author:
- Florian JUDITH (@fjudith)
extends_documentation_fragment:
- community.freetds.freetds
'''

EXAMPLES = r'''
- name: Simple select query to acme db
  community.freetds.freetds_query:
    login_db: acme
    query: SELECT * FROM orders
- name: Select query to db acme with positional arguments
  community.mysql.mysql_query:
    login_db: acme
    query: SELECT * FROM acme WHERE id = %s AND story = %s
    positional_args:
    - 1
    - test
- name: Select query to test_db with named_args
  community.mysql.mysql_query:
    login_db: test_db
    query: SELECT * FROM test WHERE id = %(id_val)s AND story = %(story_val)s
    named_args:
      id_val: 1
      story_val: test
- name: Run several insert queries against db test_db in single transaction
  community.mysql.mysql_query:
    login_db: test_db
    query:
    - INSERT INTO articles (id, story) VALUES (2, 'my_long_story')
    - INSERT INTO prices (id, price) VALUES (123, '100.00')
    single_transaction: yes
'''

RETURN = r'''
executed_queries:
    description: List of executed queries.
    returned: always
    type: list
    sample: ['select * FROM bar', 'UPDATE bar SET id = 1 WHERE id = 2']
query_result:
    description:
    - List of lists (sublist for each query) containing dictionaries
      in column:value form representing returned rows.
    returned: changed
    type: list
    sample: [[{"Column": "Value1"},{"Column": "Value2"}], [{"ID": 1}, {"ID": 2}]]
rowcount:
    description: Number of affected rows for each subquery.
    returned: changed
    type: list
    sample: [5, 1]
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.testruction.sybase.plugins.module_utils.freetds import (
    freetds_connect,
    freetds_common_argument_spec,
    freetds_driver,
    freetds_driver_fail_msg,
)
from ansible.module_utils._text import to_native

DML_QUERY_KEYWORDS = ('INSERT', 'UPDATE', 'DELETE')
# TRUNCATE is not DDL query but it also returns 0 rows affected:
DDL_QUERY_KEYWORDS = ('CREATE', 'DROP', 'ALTER', 'RENAME', 'TRUNCATE')

# ===========================================
# Module execution.
#

def main():
    argument_spec = freetds_common_argument_spec()
    argument_spec.update(
        query=dict(type='raw', required),
        database=dict(type='str'),
        positional_args=dict(type='list'),
        named_args=dict(type='dict'),
        single_transaction=dict(type='bool', default=False),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=(
        ('positionnal_args', 'named_args'), 
        ),
    )

    login_db = module.param['login_db']
    connect_timeout = module.params['connect_timeout']
    login_user = module.params['login_user']
    login_password = module.params['login_password']
    query = module.params["query"]

    if not isinstance(query, (str, list)):
            module.fail_json(msg="the query option value must be a string or list, passed %s" % type(query))

    if isinstance(query, str):
        query = [query]

    for elem in query:
        if not isinstance(elem, str):
            module.fail_json(msg="the elements in query list must be strings, passed '%s' %s" % (elem, type(elem)))
    
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
    
    if freetds_driver is None:
        module.fail_json(msg=sybase_driver_fail_msg)

    # Connect to DB:
    try:
        cursor, db_connection = sybase_connect(module, login_user, login_password,
                                              db,

                                              cursor_class='DictCursor', autocommit=autocommit)
    except Exception as e:
        module.fail_json(msg="unable to connect to database, check login_user and "
                             "login_password are correct or %s has the credentials. "
                             "Exception message: %s" % (config_file, to_native(e)))