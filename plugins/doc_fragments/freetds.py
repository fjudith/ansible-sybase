# -*- coding: utf-8 -*-

# Copyright: (c) 2015, Jonathan Mainguy <jon@soh.re>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):

    # Standard freetds documentation fragment
    DOCUMENTATION = r'''
options:
  login_user:
    description:
      - The username used to authenticate with.
    type: str
  login_password:
    description:
      - The password used to authenticate with.
    type: str
  login_host:
    description:
      - Host running the database.
    type: str
    default: localhost
  login_port:
    description:
      - Port of the Sybase server. Requires I(login_host) be defined as other than localhost if login_port is used.
    type: int
    default: 5000
  connect_timeout:
    description:
      - The connection timeout when connecting to the MySQL server.
    type: int
    default: 30
  odbc_drive:
    description:
      - Name of the driver configuration registered in /etc/odbcinst.ini
    type: str
    default: 'FreeTDS'
  encoding:
    description:
      - The ODBC connection string must be sent to the driver as a byte sequence, hence the Python string must first be encoded using the named encoding
        see U(https://docs.python.org/3/library/codecs.html#standard-encodings)
    type: str
    default: utf-16le
requirements:
   - pyodbc (Python 2.7 and Python 3.X)
notes:
   - Requires the PyODBC (Python 2.7 and Python 3.X) package installed on the remote host.
     The Python package may be installed with apt-get install freetds-dev freetds-bin unixodbc-dev tdsodbc (Ubuntu; see M(ansible.builtin.apt)) or
     yum install unixODBC unixODBC-devel freetds freetds-devel (RHEL/CentOS/Fedora; see M(ansible.builtin.yum)). You can also use dnf install python2-PyMySQL
     for newer versions of Fedora; see M(ansible.builtin.dnf).
   - Be sure you have pyodbc or pymssl library installed on the target machine
     for the Python interpreter Ansible uses, for example, if it is Python 3,
     you must install the library for Python 3. You can also change the interpreter.
     For more information, see U(https://docs.ansible.com/ansible/latest/reference_appendices/interpreter_discovery.html).
   - Both C(login_password) and C(login_user) are required when you are
     passing credentials. If none are present, the module will attempt to read
     the credentials from C(~/.odbc.ini), and finally fall back to using the MSSQL/Sybase
     default login of 'sa' with no password.
'''