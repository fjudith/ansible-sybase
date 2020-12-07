# -*- coding: utf-8 -*-

# Copyright: (c) 2015, Jonathan Mainguy <jon@soh.re>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):

    # Standard mysql documentation fragment
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
      - In some cases for local connections the I(login_unix_socket=/path/to/mysqld/socket),
        that is usually C(/var/run/mysqld/mysqld.sock), needs to be used instead of I(login_host=localhost).
    type: str
    default: localhost
  login_port:
    description:
      - Port of the MySQL server. Requires I(login_host) be defined as other than localhost if login_port is used.
    type: int
    default: 5000
  connect_timeout:
    description:
      - The connection timeout when connecting to the MySQL server.
    type: int
    default: 30
requirements:
   - myodbc (Python 2.7 and Python 3.X)
notes:
   - Requires the PyODBC (Python 2.7 and Python 3.X) package installed on the remote host.
     The Python package may be installed with apt-get install freetds-dev freetds-bin unixodbc-dev tdsodbc (Ubuntu; see M(ansible.builtin.apt)) or
     yum install unixODBC unixODBC-devel freetds freetds-devel (RHEL/CentOS/Fedora; see M(ansible.builtin.yum)). You can also use dnf install python2-PyMySQL
     for newer versions of Fedora; see M(ansible.builtin.dnf).
   - Be sure you have PyMySQL or MySQLdb library installed on the target machine
     for the Python interpreter Ansible uses, for example, if it is Python 3,
     you must install the library for Python 3. You can also change the interpreter.
     For more information, see U(https://docs.ansible.com/ansible/latest/reference_appendices/interpreter_discovery.html).
   - Both C(login_password) and C(login_user) are required when you are
     passing credentials. If none are present, the module will attempt to read
     the credentials from C(~/.my.cnf), and finally fall back to using the MySQL
     default login of 'root' with no password.
   - If there are problems with local connections, using I(login_unix_socket=/path/to/mysqld/socket)
     instead of I(login_host=localhost) might help. As an example, the default MariaDB installation of version 10.4
     and later uses the unix_socket authentication plugin by default that
     without using I(login_unix_socket=/var/run/mysqld/mysqld.sock) (the default path)
     causes the error ``Host '127.0.0.1' is not allowed to connect to this MariaDB server``.
   - Alternatively, you can use the mysqlclient library instead of MySQL-python (MySQLdb)
     which supports both Python 2.X and Python >=3.5.
     See U(https://pypi.org/project/mysqlclient/) how to install it.
'''