import os
import subprocess
import traceback
import argparse
import socket

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves import shlex_quote
from ansible.module_utils._text import to_native

executed_commands = []

# ===============================================
# Script arguments
# used for manual testing
# ===============================================
parser = argparse.ArgumentParser()
parser.parse_known_args()
parser.add_argument('-b', '--disable-table-headers', help='Disables the display of the table headers output.', default=False)
parser.add_argument('-e', '--echo-input', help='Echoes input.', default=False)
parser.add_argument('-F', '--enable-fips', help='Enables the FIPS flagger.', default=False)
parser.add_argument('-p', '--performance-statistics', help='Prints performance statistics.', default=True)
parser.add_argument('-n', '--remove-echo-numbering', help='Removes numbering and prompt symbol when used with -e', default=False)
parser.add_argument('-v', '--version', help='Prints the version number and copyright message.', default=False)
parser.add_argument('-W', '--disable-extended-password-encryption', help='Turn off extended password encryption on connection retries.', default=False)
parser.add_argument('-X', '--enable-client-side-password-encryption', help='Initiates the login connection to the server with client-side password encryption.', default=False)
parser.add_argument('-Y', '--use-chained-transactions', help='Tells the Adaptive Server to use chained transactions.', default=False)
parser.add_argument('-Q', '--enable-hafailover', help='Enables the HAFAILOVER property.', default=False)
parser.add_argument('-a', '--charset', help='Used in conjunction with -J to specify the character set translation file (.xlt file) required for the conversion. Use -a without -J only if the client character set is the same as the default character set.', default=None)
parser.add_argument('-A', '--packet-size', help='Specifies the network packet size to use for this isql session.', default=None)
parser.add_argument('-c', '--command-terminator', help='Changes the command terminator.', default='go')
parser.add_argument('-D', '--database', help='Selects the database in which the isql session begins.', default='master')
parser.add_argument('-E', '--editor', help='Specifies an editor other than the default editor vi.', default='vi')
parser.add_argument('--header', help='Specifies the number of rows to print between column headings.', default=1)
parser.add_argument('-H', '--hostname', help='Sets the client host name.', default=socket.gethostname())
parser.add_argument('-i', '--input-file', help='Specifies the name of the operating system file to use for input to isql.', default=None)
parser.add_argument('-I', '--interfaces-file', help='Specifies the name and location of the interfaces file.', default=("{0}/{1}".format(os.environ.get('SYBASE'), 'interfaces')))
parser.add_argument('-J', '--client-charset', help='Specifies the character set to use on the client.', default=None)
parser.add_argument('-K', '--keytab-file', help='Specifies the path to the keytab file used for authentication in DCE.', default=None)
parser.add_argument('-l', '--login-timeout', help='Specifies the number of seconds to wait for the server to respond to a login attempt.', default=60)
parser.add_argument('-m', '--error-message', help='Customizes the error message display.', default=None)
parser.add_argument('-M', '--label', help='(Secure SQL Server only) enables multilevel users to set the session labels for the bulk-copy', default=None)
parser.add_argument('-o', '--output-file', help='Specifies the name of an operating system file to store the output from isql.', default=None)
parser.add_argument('-P', '--password', help='Specifies your Adaptive Server password.', default=None)
parser.add_argument('-R', '--remote-server-principal', help='Specifies the principal name for the server as defined to the security mechanism.', default=None)
parser.add_argument('-s', '--column-separator', help='Resets the column separator character, which is blank by default. (for example, "|", ";", "&", "<", ">"), enclose them in quotes or precede them with a backslash.', default='|')
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
parser.add_argument('--retserverror', help='Forces isql to terminate and return a failure code when it encounters a server error of severity greater than 10.', action="store_true", default=True)
parser.add_argument('--conceal', help='Obfuscates input in an ISQL session. The optional wildcard will be used as a prompt.', default=None)
parser.add_argument('--command-encryption', help='Encrypts commands sent to a server.', action="store_true")
parser.add_argument('--appname', help='Replaces the default "isql" application name in the server with "application_name".', default="ansible_sybase_isql")
parser.add_argument('--filemode', help='Specifies the file permission for the output file, where mode is a 3-digit octal numeric value.', default=644)
parser.add_argument('--history', help='Activates command history of <length> commands in isql. With "p" history will be saved at the end of the session. --history_file file_name  Path to, and including name of the command history file.', default=0)
parser.add_argument('--binary', help='Specifies the isql binary to use. By default "isql64" will be automatically selected in favor of "isql"', default=None)
args, unknown = parser.parse_known_args()

# ===============================================
# Ansible support arguments.
# ref: https://github.com/mkleehammer/pyodbc/wiki/The-pyodbc-Module
# ===============================================
def sybase_common_argument_spec():
    return dict(
        disable_table_headers=dict(type='bool', default=args.disable_table_headers),
        echo_input=dict(type='bool', default=args.echo_input),
        enable_fips=dict(type='bool', default=args.enable_fips),
        performance_statistics=dict(type='bool', default=args.performance_statistics),
        remove_echo_numbering=dict(type='bool', default=args.remove_echo_numbering),
        version=dict(type='bool', default=args.version),
        disable_extended_password_encryption=dict(type='bool', default=args.disable_extended_password_encryption),
        enable_client_side_password_encryption=dict(type='bool', default=args.enable_client_side_password_encryption),
        use_chained_transactions=dict(type='bool', default=args.enable_client_side_password_encryption),
        enable_hafailover=dict(type='bool', default=args.enable_hafailover),
        charset=dict(type='str', default=args.charset),
        packet_size=dict(type='int', default=args.packet_size),
        command_terminator=dict(type='str', default=args.command_terminator),
        login_db=dict(type='str', default=args.database),
        editor=dict(type='str', default=args.editor),
        header=dict(type='int', default=args.header),
        hostname=dict(type='str', default=args.hostname),
        input_file=dict(type='str', default=args.input_file),
        interfaces_file=dict(type='str', default=args.interfaces_file),
        client_charset=dict(type='str', default=args.client_charset),
        keytab_file=dict(type='str', default=args.keytab_file),
        login_timeout=dict(type='int', default=args.login_timeout),
        error_message=dict(type='str', default=args.error_message),
        label=dict(type='str', default=args.label),
        output_file=dict(type='str', default=args.output_file),
        login_password=dict(type='str', no_log=args.password),
        remote_server_principal=dict(type='str', default=args.remote_server_principal),
        column_separator=dict(type='str', default=args.column_separator),
        login_server=dict(type='str', default=args.server),
        connect_timeout=dict(type='int', default=args.timeout),
        login_user=dict(type='str', default=args.username),
        data_confidentiality=dict(type='bool', default=args.data_confidentiality),
        data_integrity=dict(type='bool', default=args.data_integrity),
        mutual_authentication=dict(type='bool', default=args.mutual_authentication),
        data_origin_stamping=dict(type='bool', default=args.data_origin_stamping),
        out_of_sequence_detection=dict(type='bool', default=args.out_of_sequence_detection),
        data_replay_detection=dict(type='bool', default=args.data_replay_detection),
        credential_delegation=dict(type='bool', default=args.credential_delegation),
        column_width=dict(type='str', default=args.column_width),
        sybase_path=dict(type='str', default=args.sybase_path),
        local_name=dict(type='str', default=args.local_name),
        security_mechanism=dict(type='str', default=args.security_mechanism),
        trusted_txt_file=dict(type='str', default=args.trusted_txt_file),
        retserverror=dict(type='bool', default=args.retserverror),
        conceal=dict(type='str', default=args.conceal),
        command_encryption=dict(type='str', default=args.conceal),
        appname=dict(type='str', default=args.appname),
        filemode=dict(type='int', default=args.filemode),
        history=dict(type='int', default=args.history),
        binary=dict(type='str', default=args.binary),
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
    disable_table_headers = module.params['disable_table_headers']
    echo_input = module.params['echo_input']
    enable_fips = module.params['enable_fips']
    performance_statistics = module.params['performance_statistics']
    remove_echo_numbering = module.params['remove_echo_numbering']
    binary_version = module.params['version']
    disable_extended_password_encryption = module.params['disable_extended_password_encryption']
    enable_client_side_password_encryption = module.params['enable_client_side_password_encryption']
    use_chained_transactions = module.params['use_chained_transactions']
    enable_hafailover = module.params['enable_hafailover']
    charset = module.params['charset']
    packet_size = module.params['packet_size']
    command_terminator = module.params['command_terminator']
    login_db = module.params['login_db']
    editor = module.params['editor']
    header = module.params['header']
    hostname = module.params['hostname']
    input_file = module.params['input_file']
    interfaces_file = module.params['interfaces_file']
    client_charset = module.params['client_charset']
    keytab_file = module.params['keytab_file']
    login_timeout = module.params['login_timeout']
    error_message = module.params['error_message']
    label = module.params['label']
    output_file = module.params['output_file']
    login_password = module.params['login_password']
    remote_server_principal = module.params['remote_server_principal']
    column_separator = module.params['column_separator']
    login_server = module.params['login_server']
    connect_timeout = module.params['connect_timeout']
    login_user = module.params['login_user']
    data_confidentiality = module.params['data_confidentiality']
    data_integrity = module.params['data_integrity']
    mutual_authentication = module.params['mutual_authentication']
    data_origin_stamping = module.params['data_origin_stamping']
    out_of_sequence_detection = module.params['out_of_sequence_detection']
    data_replay_detection = module.params['data_replay_detection']
    credential_delegation = module.params['credential_delegation']
    column_width = module.params['column_width']
    sybase_path = module.params['sybase_path']
    local_name = module.params['local_name']
    security_mechanism = module.params['security_mechanism']
    trusted_txt_file = module.params['trusted_txt_file']
    retserverror = module.params['retserverror']
    conceal = module.params['conceal']
    command_encryption = module.params['command_encryption']
    appname = module.params['appname']
    filemode = module.params['filemode']
    history = module.params['history']
    binary = module.params['binary']

    changed = False

    # Sanity check
    # if len(login_db) > 1:
    #     module.fail_json(msg="Multiple databases are not supported")

    if input_file and not os.path.exists(input_file):
        module.fail_json(msg="Input file '{0}' not found".format(input_file))

    if interfaces_file and not os.path.exists(interfaces_file):
        module.fail_json(msg="Interfaces file '{0}' not found".format(interfaces_file))
    
    if keytab_file and not os.path.exists(keytab_file):
        module.fail_json(msg="Keytab file '{0}' not found".format(keytab_file))
    
    if sybase_path and not os.path.exists(sybase_path):
        module.fail_json(msg="Sybase installation directory '{0}' not found".format(sybase_path))
    
    if trusted_txt_file and not os.path.exists(trusted_txt_file):
        module.fail_json(msg="Sybase installation directory '{0}' not found".format(trusted_txt_file))
    
    # Define isql command line location
    if binary and os.path.exists("{0}/OCS-16_0/bin/{1}".format(sybase_path, binary)):
        isql_command = "{0}/OCS-16_0/bin/{1}".format(sybase_path, binary)

    elif  not binary and os.path.exists("{0}/OCS-16_0/bin/isql64".format(sybase_path)):
        isql_command = "{0}/OCS-16_0/bin/isql64".format(sybase_path)

    elif  not binary and os.path.exists("{0}/OCS-16_0/bin/isql".format(sybase_path)):
        isql_command = "{0}/OCS-16_0/bin/isql".format(sybase_path)

    else:
        module.fail_json(msg="Sybase 'isql' or 'isql64 command not found")
    
    cmd = [module.get_bin_path(isql_command, True)]

    # If version, run the command directly
    if binary_version:
        cmd.append("-v")
    else:
        if disable_table_headers:
            cmd.append("-b")
        if echo_input:
            cmd.append("-e")
        if enable_fips:
            cmd.append("-F")
        if performance_statistics:
            cmd.append("-p")
        if remove_echo_numbering:
            cmd.append("-n")
        if disable_extended_password_encryption:
            cmd.append("-W")
        if enable_client_side_password_encryption:
            cmd.append("-X")
        if use_chained_transactions:
            cmd.append("-Y")
        if enable_hafailover:
            cmd.append("-Q")
        if charset:
            cmd.append("-a {0}".format(shlex_quote(charset)))
        if packet_size:
            cmd.append("-A {0}".format(packet_size))
        if command_terminator:
            cmd.append("-c {0}".format(shlex_quote(command_terminator)))
        if login_db:
            cmd.append("-D {0}".format(shlex_quote(login_db)))
        if editor:
            cmd.append("-E {0}".format(shlex_quote(editor)))
        if header:
            cmd.append("-h {0}".format(header))
        if hostname:
            cmd.append("-H {0}".format(shlex_quote(hostname)))
        if input_file:
            cmd.append("-i {0}".format(shlex_quote(input_file)))
        if interfaces_file:
            cmd.append("-I {0}".format(shlex_quote(interfaces_file)))
        if client_charset:
            cmd.append("-I {0}".format(shlex_quote(client_charset)))
        if keytab_file:
            cmd.append("-K {0}".format(shlex_quote(keytab_file)))
        if login_timeout:
            cmd.append("-l {0}".format(login_timeout))
        if error_message:
            cmd.append("-m {0}".format(shlex_quote(error_message)))
        if label:
            cmd.append("-M {0}".format(shlex_quote(label)))
        if output_file:
            cmd.append("-o {0}".format(shlex_quote(output_file)))
        if login_password:
            cmd.append("-P {0}".format(shlex_quote(login_password)))
        if remote_server_principal:
            cmd.append("-R {0}".format(shlex_quote(remote_server_principal)))
        if column_separator:
            cmd.append("-s {0}".format(shlex_quote(column_separator)))
        if login_server:
            cmd.append("-S {0}".format(shlex_quote(login_server)))
        if connect_timeout:
            cmd.append("-t {0}".format(connect_timeout))
        if login_user:
            cmd.append("-U {0}".format(shlex_quote(login_user)))
        if data_confidentiality:
            cmd.append("-Vc")
        if data_integrity:
            cmd.append("-Vi")
        if mutual_authentication:
            cmd.append("-Vm")
        if data_origin_stamping:
            cmd.append("-Vo")
        if out_of_sequence_detection:
            cmd.append("-Vq")
        if data_replay_detection:
            cmd.append("-Vr")
        if credential_delegation:
            cmd.append("-Vd")
        if column_width:
            cmd.append("-w {0}".format(shlex_quote(column_width)))
        if sybase_path:
            cmd.append("-y {0}".format(shlex_quote(sybase_path)))
        if local_name:
            cmd.append("-z {0}".format(shlex_quote(local_name)))
        if security_mechanism:
            cmd.append("-Z {0}".format(shlex_quote(security_mechanism)))
        if trusted_txt_file:
            cmd.append("-x {0}".format(shlex_quote(trusted_txt_file)))
        if retserverror:
            cmd.append("--retserverror")
        if conceal:
            cmd.append("--conceal {0}".format(shlex_quote(conceal)))
        if command_encryption:
            cmd.append("--command-encryption")
        if appname:
            cmd.append("--appname {0}".format(shlex_quote(appname)))
        if filemode:
            cmd.append("--filemode {0}".format(filemode))
        if history:
            cmd.append("--history {0}".format(history))

    # Execute command
    cmd = ' '.join(cmd)
    executed_commands.append(cmd)
    return_code, stdout, stderr = module.run_command(cmd, use_unsafe_shell=True)
    
    if return_code != 0:
        module.fail_json(msg="{0}".format(stderr))
    module.exit_json(changed=True, msg=stdout.replace('\t','  '),
                         executed_commands=executed_commands)


if __name__ == '__main__':
    main()