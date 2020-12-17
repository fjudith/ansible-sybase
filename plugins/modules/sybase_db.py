import os
from glob import glob
import argparse
import socket
from datetime import datetime
from sys import float_repr_style

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves import shlex_quote
from ansible.module_utils._text import to_native

executed_commands = []

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
# Script arguments
# used for manual testing
# ===============================================
parser = argparse.ArgumentParser()
parser.parse_known_args()
parser.add_argument('--database', help='Is optional if the table being copied is in your default database or in master. Otherwise, specify a database name.', default=None)
parser.add_argument('--owner', help='Is optional if you or the database owner owns the table being copied. If you do not specify an owner, bcp looks first for a table of that name that you own, then looks for one owned by the database owner. If another user owns the table, specify the owner name or the command fails.', default=None)
parser.add_argument('--table', help='Is specifies the name of the database table to copy. The table name cannot be a Transact-SQL reserved word.', default=None)
parser.add_argument('--partition-id', help='Specifies the partition number into which data is to be copied. Supported only for bcp in, <partition_id> is the equivalent of <slice_number> in SAP ASE 12.5.x.', default=None)
parser.add_argument('--slice-number', help='Specifies the number of the slice of the database table into which data is to be copied. Supported only for bcp in and only for round-robin partitioned tables in SAP ASE 15.0 and later.', default=None)
parser.add_argument('--partition', help='Specifies the name of the partition in the SAP ASE server. For multiple partitions, use a comma-separated list of partition names.', default=None)
parser.add_argument('--import-data', help='Indicates a copy from a file into the database table.', default=None)
parser.add_argument('--export-data', help='Indicates a copy to a file from the database table or view.', default=None)
parser.add_argument('--datafile', help='Specifies the full path name of an operating system file. The path name can be 1 to 255 characters long. For multiple files, use a comma-separated list of file names. If you enter more than one data file and partition name, the number of files and partitions must be the same.', default=None)
parser.add_argument('-a','--display-charset', help='Allows you to run bcp from a terminal where the character set differs from that of the machine on which bcp is running. Using -a in conjunction with -J specifies the character set translation file (.xlt file) required for the conversion. Use -a without -J only if the client character set is the same as the default character set.', default=None)
parser.add_argument('-A','--packet-size', help='Specifies the network packet size to use for this bcp session.', default=None)
parser.add_argument('-b','--batchsize', help='Specifies the number of rows per batch of data copied. The largest number bcp accepts for <batchsize> is 2147483647', default=None)
parser.add_argument('-c','--char', help='Performs the copy operation using the char datatype as the default.', default=False)
parser.add_argument('-C','--bulk-copy', help='Supports bulk copy of encrypted columns if the SAP ASE server supports encrypted columns.', default=False)
parser.add_argument('-d','--discard-file-prefix', help='Logs the rejected rows into a dedicated discard file.', default=None)
parser.add_argument('-e','--error-file', help='Specifies the full path name of an error file where bcp stores any rows that it was unable to transfer from the file to the database. Error messages from bcp appear on your terminal. bcp creates an error file only when you specify this parameter.', default=None)
parser.add_argument('-E','--use-itentity', help='Explicitly specifies the value of a table’s IDENTITY column.', default=None)
parser.add_argument('-f','--format-file', help='Specifies the full path name of a file with stored responses from a previous use of bcp on the same table.', default=None)
parser.add_argument('-F','--first-row', help='Specifies the number of the first row to copy (default is the first row). If you use multiple files, this option applies to each file.', default=None)
parser.add_argument('-g','--id-start-value', help='Specifies the value of the IDENTITY column to use as a starting point for copying data in.', default=None)
parser.add_argument('-i','--input-file', help='Specifies the name of the input file.', default=None)
parser.add_argument('-I','--interfaces-file', help='Specifies the name and location of the interfaces file to search when connecting to the SAP ASE server. If you do not specify -I, bcp looks for an interfaces file (sql.ini in Windows) in the SYBASE release directory.', default=None)
parser.add_argument('-J','--client-charset', help='Specifies the character set to use on the client.', default=None)
parser.add_argument('-K','--keytab-file', help='(Used only with Kerberos security) Specifies a Kerberos keytab file that contains the security key for the user name specified with the -U option.', default=None)
parser.add_argument('-L','--last-row', help='Specifies the number of the last row to copy from an input file (default is the last row).', default=None)
parser.add_argument('--labeled', help='(secure SAP ASE only) Indicates that the data you are importing already has labels in the first field of every record.', default=False)
parser.add_argument('-m', '--max-errors', help='Specifies the maximum number of errors permitted before bcp aborts the copy.', default=10)
parser.add_argument('-M', '--session-labels', help='(secure SAP ASE only) Enables multilevel users to set the session labels for the bulk copy.', default=10)
parser.add_argument('-n', '--native', help='Performs the copy operation using native (operating system) formats. Specifying the -n parameter means bcp does not prompt for each field.', default=False)
parser.add_argument('-N', '--skip-identity', help='Skips the IDENTITY column.You cannot use both -N and -E parameters when copying data in.', default=False)
parser.add_argument('-o', '--output-file', help='Specifies the name of the output file. Standard output (stdout) is used as the default.', default=None)
parser.add_argument('-P', '--password', help='Specifies an SAP ASE password. If you do not specify -P, bcp prompts for a password. Omit the -P flag if your password is NULL.', default=None)
parser.add_argument('-Q', '--nullable', help='Provides backward compatibility with bcp for copying operations involving nullable columns.', default=False)
parser.add_argument('-r', '--row-terminator', help='Specifies the row terminator. Do not use -t or -r parameters with bcp in native format.', default=None)
parser.add_argument('-R', '--remote-server-principal', help='Specifies the principal name for the server.By default, a server’s principal name matches the server’s network name (which is specified with the -S option or the DSQUERY environment variable). Use the -R option when the server’s principal name and network name are not the same.', default=None)
parser.add_argument('-S', '--server', help='Specifies the name of the Adaptive Server to which. to connect to.', default='localhost')
parser.add_argument('-t', '--field-terminator', help='Specifies the default field terminator.', default=None)
parser.add_argument('-T', '--text-or-image-size', help='Allows you to specify, in bytes, the maximum length of text or image data that the SAP ASE server sends.', default=34816)
parser.add_argument('-U', '--username', help='Specifies an SAP ASE login name. If you do not specify this option, bcp uses the current user’s operating system login name.', default=None)
parser.add_argument('-v', '--version', help='Displays the version number of bcp and a copyright message and returns to the operating system.', default=False)
parser.add_argument('-Vi', '--data-integrity', help='Specifies network-based user authentication. Enable data integrity service.', default=False)
parser.add_argument('-Vm', '--mutual-authentication', help='Specifies network-based user authentication. Enable mutual authentication for connection establishment.', default=False)
parser.add_argument('-Vo', '--data-origin-stamping', help='Specifies network-based user authentication. Enable data origin stamping service.', default=False)
parser.add_argument('-Vq', '--out-of-sequence-detection', help='Specifies network-based user authentication. Enable out-of-sequence detection.', default=False)
parser.add_argument('-Vr', '--data-replay-detection', help='Specifies network-based user authentication. Enable data replay detection.', default=False)
parser.add_argument('-Vd', '--credential-delegation', help='Specifies network-based user authentication. Requests credential delegation and forwards client credentials.', default=False)
parser.add_argument('-W', '--disable-extended-password-encryption', help='Turn off extended password encryption on connection retries.', default=False)
parser.add_argument('-x', '--trusted-txt-file', help='Specifies an alternate trusted.txt file location.', default=None)
parser.add_argument('-X', '--enable-client-side-password-encryption', help='Initiates the login connection to the server with client-side password encryption.', default=False)
parser.add_argument('-y', '--sybase-path', help='Sets an alternate location for the Sybase home directory.', default=os.environ.get('SYBASE'))
parser.add_argument('-Y', '--disable-server-side-characterset-convertion', help='specifies that character-set conversion is disabled in the server, and is instead performed by bcp on the client side when using bcp out', action="store_true")
parser.add_argument('-z', '--local-name', help='Sets the official name of an alternate language to display isql prompts and messages.', default=None)
parser.add_argument('-Z', '--security-mechanism', help='Specifies the security mechanism names are defined in the libtcl.cfg configuration file located in the $SYBASE/ini directory.', default=None)
parser.add_argument('--colpasswd', help='Sets the passwords for encrypted columns by sending set encryption passwd <password> for column <column_name> to the SAP ASE server.', default=None)
parser.add_argument('--hide-vcc', help='Instructs bcp not to copy virtual computed columns (VCC) either to or from a data file. ', action="store_true")
parser.add_argument('--initstring', help='Sends Transact-SQL commands to the SAP ASE server before data is transferred.', default=None)
parser.add_argument('--keypasswd', help='Sets passwords for all columns accessed by a key by sending set encryption passwd <password> for key <key_name> to the SAP ASE server.', default=None)
parser.add_argument('--maxconn', help='Is the maximum number of parallel connections permitted for each bulk copy operation.', default=None)
parser.add_argument('--show-fi', help='Instructs bcp to copy functional indexes, while using either bcp in or bcp out.', action="store_true")
parser.add_argument('--skiprows', help='Instructs bcp to skip a specified number of rows before starting to copy from an input file.', default=None)
parser.add_argument('--binary', help='Specifies the isql binary to use. By default "bcp64" will be automatically selected in favor of "bcp"', default=None)
parser.add_argument('--host', help='Specifies the hostname or IP address of the target database server', default='localhost')
parser.add_argument('--port', help='Specifies the port to connect to the target database server.', default=5000)
parser.add_argument('--driver', help='Specifies the ODBC driver to use from the "/etc/odbcinst" or "~/odbcinst" configuration file.', default='FreeTDS')
parser.add_argument('--encoding', help='Specifies the character encoding for the ODBC connection.', default='utf-16le')
parser.add_argument('--connect-timeout', help='Specifies the connexion timeout in seconds.', default=30)
args, unknown = parser.parse_known_args()

# ===============================================
# Ansible support arguments.
# ref: https://help.sap.com/viewer/da6c1d172bef4597a78dc5e81a9bb947/16.0.2.9/en-US/a7e76026bc2b1014ab4fb94d2d25b198.html
# ===============================================
def sybase_common_argument_spec():
    return dict(
        login_db=dict(type='str', default=args.database, aliases=['db', 'database']),
        owner=dict(type='str', default=args.owner),
        table=dict(type='str', default=args.table),
        partition_id=dict(type='int', default=args.partition_id),
        slice_number=dict(type='int', default=args.slice_number),
        partition=dict(type='bool', default=args.partition),
        datafile=dict(type='list', default=args.datafile)
        import_data=dict(type='bool', default=args.import_data),
        export_data=dict(type='bool', default=args.export_data),
        datafile=dict(type='str', default=args.export_data),
        display_charset=dict(type='str', default=args.display_charset),
        packet_size=dict(type='int', default=args.packet_size),
        batchsize=dict(type='int', default=args.batchsize),
        char=dict(type='bool', default=args.char),
        bulk_copy=dict(type='bool', default=args.bulk_copy),
        discard_file_prefix=dict(type='str', default=args.discard_file_prefix),
        error_file=dict(type='str', default=args.error_file),
        use_itentity=dict(type='bool', default=args.use_itentity),
        format_file=dict(type='str', default=args.format_file),
        first_row=dict(type='int', default=args.first_row),
        id_start_value=dict(type='str', default=args.id_start_value),
        input_file=dict(type='str', default=args.input_file),
        interfaces_file=dict(type='str', default=args.interfaces_file),
        client_charset=dict(type='str', default=args.client_charset),
        keytab_file=dict(type='str', default=args.keytab_file),
        last_row=dict(type='int', default=args.last_row),
        labeled=dict(type='bool', default=args.labeled),
        max_errors=dict(type='int', default=args.max_errors),
        session_labels=dict(type='str', default=args.session_labels),
        native=dict(type='bool', default=args.native),
        skip_identity=dict(type='bool', default=args.skip_identity),
        output_file=dict(type='str', default=args.output_file),
        login_password=dict(type='str', no_log=args.password, aliases=['pass', 'password']),
        nullable=dict(type='str', default=args.nullable),
        row_terminator=dict(type='str', default=args.row_terminator),
        remote_server_principal=dict(type='str', default=args.remote_server_principal),
        server=dict(type='str', default=args.server),
        field_terminator=dict(type='str', default=args.field_terminator),
        text_or_image_size=dict(type='str', default=args.text_or_image_size),
        login_user=dict(type='str', default=args.username, aliases=['user', 'username']),
        version=dict(type='bool', default=args.version),
        data_confidentiality=dict(type='bool', default=args.data_confidentiality),
        data_integrity=dict(type='bool', default=args.data_integrity),
        mutual_authentication=dict(type='bool', default=args.mutual_authentication),
        data_origin_stamping=dict(type='bool', default=args.data_origin_stamping),
        out_of_sequence_detection=dict(type='bool', default=args.out_of_sequence_detection),
        data_replay_detection=dict(type='bool', default=args.data_replay_detection),
        credential_delegation=dict(type='bool', default=args.credential_delegation),
        disable_extended_password_encryption=dict(type='bool', default=args.disable_extended_password_encryption),    
        trusted_txt_file=dict(type='str', default=args.trusted_txt_file),
        enable_client_side_password_encryption=dict(type='bool', default=args.enable_client_side_password_encryption),
        sybase_path=dict(type='str', default=args.sybase_path),
        disable_server_side_characterset_convertion=dict(type='bool', default=args.disable_server_side_characterset_convertion),
        local_name=dict(type='str', default=args.local_name),
        security_mechanism=dict(type='str', default=args.security_mechanism),
        colpasswd=dict(type='str', no_log=args.colpasswd),
        hide_vcc=dict(type='bool', default=args.hide_vcc),
        keypasswd=dict(type='str', no_log=args.keypasswd),
        initstring=dict(type='str', no_log=args.initstring),
        maxconn=dict(type='int', default=args.maxconn),
        show_fi=dict(type='bool', default=args.show_fi),
        skip_rows=dict(type='list', default=args.show_fi),
        binary=dict(type='str', default=args.binary),
        login_host=dict(type='str', default=args.login_host, aliases=['host', 'hostname']),
        login_port=dict(type='int', default=args.login_port, aliases=['port']),
        odbc_driver=dict(type='str', default=args.driver, aliases=['driver']),
        odbc_encoding=dict(type='str', default=args.encoding, aliases=['encoding']),
        connect_timeout=dict(type='str', default=args.connect_timeout, aliases=['timeout']),
        state=dict(type='str', default='present', choices=['absent', 'dump', 'export', 'out' 'import', 'in', 'present']),
        )


# ===============================================
# Compute base bcp command.
# ===============================================
def command_primary_spec(module):
    binary = module.params['binary']
    login_db = module.params['login_db']
    owner = module.params['owner']
    table = module.params['table']
    partition_id = module.params['partition_id']
    slice_number = module.params['slice_number']
    partition = module.params['partition']
    version = module.params['version']
    
    # Define bcp command line location
    if binary and os.path.exists("{0}/OCS-16_0/bin/{1}".format(sybase_path, binary)):
        bcp_command = "{0}/OCS-16_0/bin/{1}".format(sybase_path, binary)

    elif  not binary and os.path.exists("{0}/OCS-16_0/bin/bcp64".format(sybase_path)):
        bcp_command = "{0}/OCS-16_0/bin/bcp64".format(sybase_path)

    elif  not binary and os.path.exists("{0}/OCS-16_0/bin/bcp".format(sybase_path)):
        bcp_command = "{0}/OCS-16_0/bin/bcp".format(sybase_path)

    else:
        module.fail_json(msg="Sybase 'bcp' or 'bcp64 command not found")
    
    cmd = [module.get_bin_path(bcp_command, True)]

    # If version, run the command directly
    if version:
        cmd.append("-v")
    else:
        if login_db and owner and table:
            cmd.append("{0}.{1}.{2}".format(login_db, owner, table))
        elif login_db and owner:
            cmd.append("{0}.{1}".format(login_db, owner))
        elif login_db:
            cmd.append("{0}".format(login_db))
        
        if partition_id:
            cmd.append(": {0}".format(partition_id))
        elif slice_number:
            cmd.append(": {0}".format(slice_number))

        if partition:
            cmd.append("partition {0}".format(partition))
    
    return cmd

# ===============================================
# Check if database exists
# ===============================================
def check_database_exists(cursor, database):
    res = 0
    for item in database:
        res += cursor.execute("select * form sysobjects where name='{0}'".format(item))
    return res == len(database)

# ===============================================
# Remove database
# ===============================================
def remove_database(cursor, database):
    if not database:
        return False
    for item in database:
        res += cursor.execute("drop database {0}".format(sybase_quote_identifier(item, 'database')))
    return True

# ===============================================
# Create database
# ===============================================
def create_database(cursor, database, size=None):
    if not database:
        return False
    res = 0
    for each_db in db:
        query = ['create database {0}'.format(sybase_quote_identifier(each_db, 'database'))]
        if size:
            query.append("= '{0}'".format(size))
        query = ' '.join(query)
        res += cursor.execute(query)
        try:
            executed_commands.append(cursor.mogrify(query))
        except AttributeError:
            executed_commands.append(cursor._executed)
        except Exception:
            executed_commands.append(query)
    return res > 0

# ===============================================
# Module execution.
# ===============================================
def main():
    # Prepare parameters
    argument_spec = sybase_common_argument_spec()
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=(
            ('partition_id', 'slice_number'), 
        ),
        supports_check_mode=True,
    )

    # Mandatory parameters
    state = module.params["state"]
    login_db = module.params["login_db"]
    owner = module.params["owner"]
    table = module.params["table"]
    partition_id = module.params["partition_id"]
    slice_number = module.params["slice_number"]
    partition = module.params["partition"]
    datafile = module.params["datafile"]
    display_charset = module.params["display_charset"]
    packet_size = module.params["packet_size"]
    batchsize = module.params["batchsize"]
    char = module.params["char"]
    bulk_copy = module.params["bulk_copy"]
    discard_file_prefix = module.params["discard_file_prefix"]
    error_file = module.params["error_file"]
    use_itentity = module.params["use_itentity"]
    format_file = module.params["format_file"]
    first_row = module.params["first_row"]
    id_start_value = module.params["id_start_value"]
    input_file = module.params["input_file"]
    interfaces_file = module.params["interfaces_file"]
    client_charset = module.params["client_charset"]
    keytab_file = module.params["keytab_file"]
    last_row = module.params["last_row"]
    labeled = module.params["labeled"]
    max_errors = module.params["max_errors"]
    session_labels = module.params["session_labels"]
    native = module.params["native"]
    skip_identity = module.params["skip_identity"]
    output_file = module.params["output_file"]
    login_password = module.params["login_password"]
    nullable = module.params["nullable"]
    row_terminator = module.params["row_terminator"]
    remote_server_principal = module.params["remote_server_principal"]
    server = module.params["server"]
    field_terminator = module.params["field_terminator"]
    text_or_image_size = module.params["text_or_image_size"]
    login_user = module.params["login_user"]
    version = module.params["version"]
    data_confidentiality = module.params["data_confidentiality"]
    data_integrity = module.params["data_integrity"]
    mutual_authentication = module.params["mutual_authentication"]
    data_origin_stamping = module.params["data_origin_stamping"]
    out_of_sequence_detection = module.params["out_of_sequence_detection"]
    data_replay_detection = module.params["data_replay_detection"]
    credential_delegation = module.params["credential_delegation"]
    disable_extended_password_encryption = module.params["disable_extended_password_encryption"]
    trusted_txt_file = module.params["trusted_txt_file"]
    enable_client_side_password_encryption = module.params["enable_client_side_password_encryption"]
    sybase_path = module.params["sybase_path"]
    disable_server_side_characterset_convertion = module.params["disable_server_side_characterset_convertion"]
    local_name = module.params["local_name"]
    security_mechanism = module.params["security_mechanism"]
    colpasswd = module.params["colpasswd"]
    hide_vcc = module.params["hide_vcc"]
    initstring = module.params["initstring"]
    keypasswd = module.params["keypasswd"]
    maxconn = module.params["maxconn"]
    show_fi = module.params["show_fi"]
    skip_rows = module.params["skip_rows"]
    binary = module.params["binary"]
    login_host = module.params["login_host"]
    login_port = module.params["login_port"]
    odbc_driver = module.params["odbc_driver"]
    odbc_encoding = module.params["odbc_encoding"]
    connect_timeout = module.params["connect_timeout"]

    changed = False
    started = datetime.now()

    # Check ODBC driver initialization
    if sybase_driver is None:
        module.fail_json(msg=sybase_driver_fail_msg)

    # Sanity check
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
    
    if error_file and not os.path.exists(error_file):
        module.fail_json(msg="Error file '{0}' not found".format(error_file))
    
    if discard_file_prefix and not bool(glob(discard_file_prefix + '*')):
        module.fail_json(msg="One or more Discard file '{0}*' not found".format(discard_file_prefix))
    
    if format_file and not os.path.exists(format_file):
        module.fail_json(msg="Format file '{0}' not found".format(format_file))

    if len(login_db) > 1 and state == 'import':
        module.fail_json(msg="Multiple databases are not supported with state=import")
    
    # Initialize bcp command arguments
    cmd = [command_primary_spec()]

    if not binary_version:
        if state in ['dump', 'export', 'out', 'import', 'in']:
            if not server:
                module.fail_json(msg="with state={0} 'server' is required".format(state))
    
        # Connect to Database:
        try:
            db_connection = sybase_driver.connect(driver=odbc_driver, user=login_user, password=login_password,
                                                host=login_host, port=login_port, database=login_db,
                                                connect_timeout=connect_timeout, odbc_encoding=odbc_encoding)
        except Exception as e:
            module.fail_json(msg="unable to connect to database: '%s', check login_user and "
                                "login_password are correct."
                                "ODBC driver: '%s'. Exception message: '%s'" % (login_db, odbc_driver, to_native(e)))

        existence_list = []
        non_existence_list = []

        # Get cursor
        cursor = db_connection.cursor()

        # List existing and non-existing databases
        for each db in login_db:
            if check_database_exists(cursor, [db]):
                existence_list.append(db)
            else:
                non_existence_list.append(db)
        
        if state == 'absent':
            if module.checkmode:
                module.exit_json(changed=bool(existence_list), db=db_name, db_list=login_db)
            try:
                changed = remove_database(cursor, existence_list)
            except Exception as e:
                module.fail_json(msg="Error deleting database: %s" % to_native(e))
            module.exit_json(changed=changed, db=db_name, db_list=login_db, executed_commands=executed_commands)
        
        elif state == "present":
            if module.check_mode:
                module.exit_json(changed=bool(non_existence_list), db=db_name, db_list=login_db)
            changed = False
            if non_existence_list:
                try:
                    changed = create_database(cursor, non_existence_list)
                except Exception as e:
                    module.fail_json(msg="error creating database: %s" % to_native(e),
                                     exception=traceback.format_exc())
            module.exit_json(changed=changed, db=db_name, db_list=login_db, executed_commands=executed_commands)
        
        elif state in ['dump','export', 'out']:
            if non_existence_list:
                module.fail_json(msg="Cannot dump database(s) %r - not found" % (', '.join(non_existence_list)))
            if module.check_mode:
                module.exit_json(changed=True, db=db_name, db_list=login_db)
            cmd.append('out')

        elif state in ['import', 'in']:
            if module.check_mode:
                module.exit_json(changed=True, db=db_name, db_list=login_db)
            if non_existence_list and not all_databases:
                try:
                    create_database(cursor, non_existence_list)
                except Exception as e:
                    module.fail_json(msg="Error creating database: %s" % to_native(e),
                                     exception=traceback.format_exc())
            cmd.append('in')

        # bool: cmd.append("-x")
        # int: cmd.append("-x {0}".format(var))
        # str: cmd.append("-x {0}".format(shlex_quote(var)))
        if datafile:
            cmd.append("{0}".format(shlex_quote(datafile.join(','))))
        if display_charset:
            cmd.append("-a {0}".format(shlex_quote(display_charset)))
        if packet_size:
            cmd.append("-A {0}".format(packet_size))
        if batchsize:
            cmd.append("-b {0}".format(batchsize))
        if char:
            cmd.append("-c")
        if bulk_copy:
            cmd.append("-C")
        if discard_file_prefix:
            cmd.append("-d {0}".format(shlex_quote(discard_file_prefix)))
        if error_file:
            cmd.append("-e {0}".format(shlex_quote(error_file)))
        if use_itentity:
            cmd.append("-E")
        if format_file:
            cmd.append("-f {0}".format(shlex_quote(format_file)))
        if first_row:
            cmd.append("-F {0}".format(first_row))
        if id_start_value:
            cmd.append("-g {0}".format(id_start_value))
        if input_file:
            cmd.append("-i {0}".format(shlex_quote(intput_file)))
        if interfaces_file:
            cmd.append("-I {0}".format(shlex_quote(interfaces_file)))
        if client_charset:
            cmd.append("-J {0}".format(shlex_quote(client_charset)))
        if keytab_file:
            cmd.append("-K {0}".format(shlex_quote(keytab_file)))
        if last_row:
            cmd.append("-L {0}".format(last_row))
        if max_errors:
            cmd.append("-m {0}".format(max_errors))
        if labeled:
            cmd.append("-labeled")
        if session_labels:
            cmd.append("-M {0}".format(shlex_quote(session_labels)))
        if native:
            cmd.append("-n")
        if skip_identity:
            cmd.append("-N")
        if output_file:
            cmd.append("-o {0}".format(shlex_quote(output_file)))
        if login_password:
            cmd.append("-o {0}".format(shlex_quote(password)))
        if nullable:
            cmd.append("-Q")
        if row_terminator:
            cmd.append("-r {0}".format(shlex_quote(row_terminator)))
        if remote_server_principal:
            cmd.append("-R {0}".format(shlex_quote(remote_server_principal)))
        if server:
            cmd.append("-S {0}".format(shlex_quote(server)))
        if field_terminator:
            cmd.append("-t {0}".format(shlex_quote(field_terminator)))
        if text_or_image_size:
            cmd.append("-T {0}".format(text_or_image_size))
        if login_user:
            cmd.append("-t {0}".format(shlex_quote(login_user)))
        if login_user:
            cmd.append("-t {0}".format(shlex_quote(login_user)))
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
        if disable_extended_password_encryption:
            cmd.append("-W")
        if trusted_txt_file:
            cmd.append("-x {0}".format(shlex_quote(trusted_txt_file)))
        if enable_client_side_password_encryption:
            cmd.append("-X")
        if sybase_path:
            cmd.append("-y {0}".format(shlex_quote(sybase_path)))
        if disable_server_side_characterset_convertion:
            cmd.append("-Y")
        if local_name:
            cmd.append("-z {0}".format(shlex_quote(local_name)))
        if security_mechanism:
            cmd.append("-Z {0}".format(shlex_quote(security_mechanism)))
        if colpasswd:
            cmd.append("--colpasswd {0}".format(shlex_quote(colpasswd)))
        if keypasswd:
            cmd.append("--colpasswd {0}".format(shlex_quote(keypasswd)))
        if hide_vcc:
            cmd.append("--hide-vcc")
        if initstring:
            cmd.append("--initstring {0}".format(shlex_quote(initstring)))
        if maxconn:
            cmd.append("--maxconn {0}".format(maxconn))
        if show-fi:
            cmd.append("--show-fi")
        if skip_rows:
            cmd.append("{0}".format(shlex_quote(skip_rows.join(','))))
    
    # Execute bcp command
    if state in ['dump', 'export', 'out', 'import', 'in']:
        cmd = ' '.join(cmd)
        executed_commands.append(cmd)
        return_code, stdout, stderr = module.run_command(cmd, use_unsafe_shell=True)
    
    finished = datetime.now()
    difference = (finished - started)

    if return_code != 0:
        module.fail_json(msg="{0}".format(stderr),
                         start=str(started),
                         end=str(finished),
                         db_list=login_db,
                         duration=str(difference.resolution)
                         )
    changed = True
    module.exit_json(changed=changed,
                     msg=stdout.replace('\t','  '),
                     executed_commands=executed_commands,
                     start=str(started),
                     end=str(finished),
                     duration=str(difference.resolution)
                     )

if __name__ == '__main__':
    main()