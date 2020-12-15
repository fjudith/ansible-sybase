import os
import subprocess
import traceback
import argparse
import socket

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves import shlex_quote
from ansible.module_utils._text import to_native

# ===============================================
# Script arguments
# used for manual testing
# ===============================================
parser = argparse.ArgumentParser()
parser.parse_known_args()
parser.add_argument('-b', '--disable-table-headers', help='Disables the display of the table headers output.', default=False)
parser.add_argument('-e', '--echo-input', help='Echoes input.', default=False)
parser.add_argument('-F', '--enable-FIPS', help='Enables the FIPS flagger.', default=False)
parser.add_argument('-p', '--performance-statics', help='Prints performance statistics.', default=False)
parser.add_argument('-n', '--remove-echo-numbering', help='Removes numbering and prompt symbol when used with -e', default=False)
parser.add_argument('-v', '--version', help='Prints the version number and copyright message.', default=False)
parser.add_argument('-W', '--disable-extended-password-encryption', help='Turn off extended password encryption on connection retries.', default=False)
parser.add_argument('-X', '--enable-client-side-password-encryption', help='Initiates the login connection to the server with client-side password encryption.', default=False)
parser.add_argument('-Y', '--use-chained-transactions', help='Tells the Adaptive Server to use chained transactions.', default=False)
parser.add_argument('-Q', '--enable-hafailover', help='Enables the HAFAILOVER property.', default=False)
parser.add_argument('-a', '--charset', help='Used in conjunction with -J to specify the character set translation file (.xlt file) required for the conversion. Use -a without -J only if the client character set is the same as the default character set.', default=False)
parser.add_argument('-A', '--packet-size', help='Specifies the network packet size to use for this isql session.', default=False)
parser.add_argument('-c', '--command-terminator', help='Changes the command terminator.', default='go')
parser.add_argument('-D', '--database', help='Selects the database in which the isql session begins.', default='master')
parser.add_argument('-E', '--editor', help='Specifies an editor other than the default editor vi.', default='vi')
parser.add_argument('-h', '--header', help='Specifies the number of rows to print between column headings.', default='1')
parser.add_argument('-H', '--hostname', help='Sets the client host name.', default=socket.gethostname())
parser.add_argument('-i', '--intput-file', help='Specifies the name of the operating system file to use for input to isql.', default=None)
parser.add_argument('-I', '--interfaces-file', help='Specifies the name and location of the interfaces file.', default=("{0}/{1}".format(os.environ.get('SYBASE'), 'interfaces')))
parser.add_argument('-J', '--client-charset', help='Specifies the character set to use on the client.', default=None)
parser.add_argument('-K', '--keytab-file', help='Specifies the path to the keytab file used for authentication in DCE.', default=None)
parser.add_argument('-l', '--login-timeout', help='Specifies the number of seconds to wait for the server to respond to a login attempt.', default=60)
parser.add_argument('-m', '--error-message', help='Customizes the error message display.', default=None)
parser.add_argument('-M', '--label', help='(Secure SQL Server only) enables multilevel users to set the session labels for the bulk-copy', default=None)
parser.add_argument('-o', '--output-file', help='Specifies the name of an operating system file to store the output from isql.', default=None)
parser.add_argument('-P', '--password', help='Specifies your Adaptive Server password.', default=None)
parser.add_argument('-R', '--remote-server-principal', help='Specifies the principal name for the server as defined to the security mechanism.', default=None)
parser.add_argument('-s', '--column-separator', help='Resets the column separator character, which is blank by default. (for example, "|", ";", "&", "<", ">"), enclose them in quotes or precede them with a backslash.', default=None)
parser.add_argument('-S', '--server', help='Specifies the name of the Adaptive Server to which. to connect to.', default='localhost')
parser.add_argument('-t', '--timeout', help='Specifies the number of seconds before a SQL command times out.', default=60)
parser.add_argument('-U', '--username', help='Specifies a login name. Login names are case sensitive.', default='sa')
parser.add_argument('-Vc', '--data-confidentiality', help='Specifies network-based user authentication. Enable data confidentiality service.', default=False)
parser.add_argument('-Vi', '--data-integrity', help='Specifies network-based user authentication. Enable data integrity service.', default=False)
parser.add_argument('-Vm', '--mutual-authentication', help='Specifies network-based user authentication. Enable mutual authentication for connection establishment.', default=False)
parser.add_argument('-Vo', '--data-origin-stamping', help='Specifies network-based user authentication. Enable data origin stamping service.', default=False)
parser.add_argument('-Vq', '--out-of-sequence-detection', help='Specifies network-based user authentication. Enable out-of-sequence detection.', default=False)
parser.add_argument('-Vr', '--data-replay-detection', help='Specifies network-based user authentication. Enable data replay detection.', default=False)
parser.add_argument('-Vd', '--credential-delegation', help='Specifies network-based user authentication. Requests credential delegation and forwards client credentials.', default=False)
parser.add_argument('-w', '--column-width', help='Sets the screen width for output.', default=80)
parser.add_argument('-y', '--sybase-path', help='Sets an alternate location for the Sybase home directory.', default=os.environ.get('SYBASE'))
parser.add_argument('-z', '--local-name', help='Sets the official name of an alternate language to display isql prompts and messages.', default=None)
parser.add_argument('-Z', '--security-mechanism', help='Specifies the security mechanism names are defined in the libtcl.cfg configuration file located in the $SYBASE/ini directory.', default=None)
parser.add_argument('-x', '--trusted-txt-file', help='Specifies an alternate trusted.txt file location.', default=None)
parser.add_argument('--retserverror', help='Forces isql to terminate and return a failure code when it encounters a server error of severity greater than 10.', action="store_true")
parser.add_argument('--conceal', help='Obfuscates input in an ISQL session. The optional wildcard will be used as a prompt.', default=None)
parser.add_argument('--command_encryption', help='Encrypts commands sent to a server.', action="store_true")
parser.add_argument('--appname', help='Replaces the default "isql" application name in the server with "application_name".', default="ansible_isql")
parser.add_argument('--filemode', help='Specifies the file permission for the output file, where mode is a 3-digit octal numeric value.', default=644)
parser.add_argument('--history', help='Activates command history of <length> commands in isql. With 'p' history will be saved at the end of the session. --history_file file_name  Path to, and including name of the command history file.', default=0)
args, unknown = parser.parse_known_args()

# ===============================================
# Ansible support arguments.
# ref: https://github.com/mkleehammer/pyodbc/wiki/The-pyodbc-Module
# ===============================================
def sybase_common_argument_spec():
    return dict(
        login_user=dict(type='str', default=args.username),
        login_password=dict(type='str', no_log=args.password),
        login_server=dict(type='str', default=args.server),
        login_db=dict(type='str', default=args.database),
        connect_timeout=dict(type='int', default=args.timeout),
        input_file=dict(type='str', default=args.input_file),
        column_width=dict(type='int', default=args.column_width),
        sybase_path=dict(type='str', default=args.sybase_path),
        interfaces_files=dict(type='str', default=args.interfaces_files),
        login_timeout=dict(type='str', default=args.login_timeout),
    )

# ===============================================
# Module execution.
# ===============================================
def main():
    # Prepare parameters
    argument_spec = sybase_common_argument_spec()
    module = AnsibleModule(
        argument_spec=argument_spec
        # mutually_exclusive=(
        #     ('version', 'version'), 
        # ),
    )

    # Mandatory parameters
    login_host       = module.params['login_host']
    login_port       = module.params['login_port']
    login_user       = module.params['login_user']
    login_password   = module.params['login_password']
    login_db         = module.params['login_db']
    connect_timeout  = module.params['connect_timeout']
    column_width     = module.params['column_width']
    sybase_path      = module.params['sybase_path']
    interfaces_files = module.params['interfaces_files']
    login_timeout    = module.params['login_timeout']

if __name__ == '__main__':
    main()