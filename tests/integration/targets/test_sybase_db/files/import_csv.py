import os
import argparse
import logging
import pyodbc
import csv
from datetime import datetime

driver='FreeTDS'

parser = argparse.ArgumentParser()
parser.parse_known_args()
# Input file related arguments
parser.add_argument('-f', '--filename', help='that contains the data to import', default=os.environ.get('FK_FILENAME', default=None ))
parser.add_argument('--comma-csv', help="CSV formatted file format", action="store_true", default=True)
parser.add_argument('--comma-delimited', help="comma ',' delimited file format", action="store_true")
parser.add_argument('--pipe-delimited', help="Pipe '|' delimited file format", action="store_true")
# SQL related arguments
parser.add_argument('-S', '--server', help='target SQL server', default=os.environ.get('FK_SERVER', default="127.0.0.1"))
parser.add_argument('-P', '--port', help='listen port port of the SQL service', default=os.environ.get('FK_PORT', default="5000"))
parser.add_argument('-D', '--database', help='taget SQL database', default=os.environ.get('FK_DATABASE', default="fakenames"))
parser.add_argument('-T', '--table', help='listen port port of the SQL service', default=os.environ.get('FK_TABLE', default="fakenames"))
parser.add_argument('-u', '--username', help='to authenticate to the SQL database', default=os.environ.get('FK_USERNAME', default="sa"))
parser.add_argument('-p', '--password', help='to access to the SQL database', default=os.environ.get('FK_PASSWORD', default="myPassword"))
# Logger arguments
parser.add_argument('-d', '--debug', help="Enable debug logging", action="store_true")
args, unknown = parser.parse_known_args()

logger = logging.getLogger('script')
ch = logging.StreamHandler()
if args.debug:
    logger.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
    ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def connect():
    # Connect to database
    logger.info('Connecting to server "{0}:{1}" database "{2}"'.format(args.server, args.port, args.database))
    conn = pyodbc.connect(driver=driver, server=args.server, database=args.database ,port=args.port, uid=args.username, pwd=args.password)
    return conn


def create_table(dbconn, tablename):
    logger.info('Check if table "{0}" exists'.format(tablename))
    
    cursor = dbconn.cursor()
    
    cursor.execute("""
        select name
        from sysobjects
        where type = "U" and name = '{0}'
        """.format(tablename)
    )
    
    try: 
        cursor.fetchone()[0]

        logger.info('Table "{0}" already exists.'.format(tablename))
    except TypeError as e:
        logger.info('Table "{0}" does not exists. Creating...'.format(tablename))

        cursor.execute("""
        CREATE TABLE {0} (
        number numeric (10,0) identity primary key,
        gender nvarchar(6) not null,
        nameset nvarchar(25) not null,
        title nvarchar(6) not null,
        givenname nvarchar(20) not null,
        middleinitial nvarchar(1) not null,
        surname nvarchar(23) not null,
        streetaddress nvarchar(100) not null,
        city nvarchar(100) not null,
        state nvarchar(22) not null,
        statefull nvarchar(100) not null,
        zipcode nvarchar(15) not null,
        country nvarchar(2) not null,
        countryfull nvarchar(100) not null,
        emailaddress nvarchar(100) not null,
        username varchar(25) not null,
        password nvarchar(25) not null,
        browseruseragent nvarchar(255) not null,
        telephonenumber nvarchar(25) not null,
        telephonecountrycode int not null,
        maidenname nvarchar(23) not null,
        birthday datetime not null,
        age int not null,
        tropicalzodiac nvarchar(11) not null,
        cctype nvarchar(10) not null,
        ccnumber nvarchar(16) not null,
        cvv2 nvarchar(3) not null,
        ccexpires nvarchar(10) not null,
        nationalid nvarchar(20) not null,
        upstracking nvarchar(24) not null,
        westernunionmtcn nchar(10) not null,
        moneygrammtcn nchar(8) not null,
        color nvarchar(6) not null,
        occupation nvarchar(70) not null,
        company nvarchar(70) not null,
        vehicle nvarchar(255) not null,
        domain nvarchar(70) not null,
        bloodtype nvarchar(3) not null,
        pounds decimal(5,1) not null,
        kilograms decimal(5,1) not null,
        feetinches nvarchar(6) not null,
        centimeters smallint not null,
        guid nvarchar(36) not null,
        latitude numeric(10,8) not null,
        longitude numeric(11,8) not null
        )
        """.format(tablename))

        dbconn.commit()
        

def import_pipe_delimited_data(dbconn, tablename, filename):
    logger.info('Load data from file "{0}" to table "{1}"'.format(filename, tablename))
    started = datetime.now()

    # Table configuration
    cursor = dbconn.cursor()
    cursor.execute('SET IDENTITY_INSERT {0} ON'.format(tablename))
    cursor.commit()

    # Count total number of lines in the input file
    with open (file=filename, mode='r', newline=None, encoding='utf-8-sig') as f:
        reader = csv.reader(f, delimiter='|', quotechar='"')
        next(reader)
        lines = len(list(reader))
        

    with open (file=filename, mode='r', newline=None, encoding='utf-8-sig') as f:
        reader = csv.reader(f, delimiter='|', quotechar='"')
        columns = next(reader)
        query = 'insert into ' + tablename + '({0}) values ({1})'
        query = query.format(','.join(columns), ','.join('?' * len(columns))).lower()
        query = query.replace('mothersmaiden','maidenname')
        query = query.replace('ups','upstracking')
        
        logger.info('Processing "{0}" lines'.format(lines))
        record = 0

        for data in reader:
            cursor = dbconn.cursor()
        
            data[0] = int(data[0])                # number
            data[8] = data[8].replace('Ÿ','Y')    # city
            data[15] = data[15].replace('œ','oe') # password
            data[19] = int(data[19])              # telephonecountrycode
            data[22] = int(data[22])              # age
            data[38] = float(data[38])            # pounds
            data[39] = float(data[39])            # kilograms
            data[41] = int(data[41])              # centimeters
            data[43] = float(data[43])            # latitude
            data[44] = float(data[44])            # longitude
            
            cursor.execute(query, data)
            cursor.commit()
            record += 1

    finished = datetime.now()
    difference = (finished - started)
    logger.info('Imported {0}/{1} line from file "{2}" to table "{3}" in "{4}"'.format(record, lines, filename, tablename, difference))


def import_csv_delimited_data(dbconn, tablename, filename):
    logger.info('Load CSV data from file "{0}" to table "{1}"'.format(filename, tablename))
    started = datetime.now()

    # Table configuration
    cursor = dbconn.cursor()
    cursor.execute('SET IDENTITY_INSERT {0} ON'.format(tablename))
    cursor.commit()

    # Count total number of lines in the input file
    with open (file=filename, mode='r', newline=None, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        lines = len(list(reader))

    with open (file=filename, mode='r', newline=None, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        query = 'insert into ' + tablename + '({0}) values ({1})'
        query = query.format(','.join(reader.fieldnames), ','.join('?' * len(reader.fieldnames))).lower()
        query = query.replace('mothersmaiden','maidenname')
        query = query.replace('ups','upstracking')

        logger.info('Processing "{0}" lines'.format(lines))
        record = 0
        
        for data in reader:
            cursor = dbconn.cursor()
        
            data['Number'] = int(data['Number'])
            data['City'] = data['City'].replace('Ÿ','Y')
            data['Password'] = data['Password'].replace('œ','oe')
            data['TelephoneCountryCode'] = int(data['TelephoneCountryCode'])
            data['Age'] = int(data['Age'])
            data['Pounds'] = float(data['Pounds'])
            data['Kilograms'] = float(data['Kilograms'])
            data['Centimeters'] = int(data['Centimeters'])
            data['Latitude'] = float(data['Latitude'])
            data['Longitude'] = float(data['Longitude'])
            
            cursor.execute(query, list(data.values()))
            cursor.commit()
            record += 1

    finished = datetime.now()
    difference = (finished - started)
    logger.info('Imported {0}/{1} line from file "{2}" to table "{3}" in "{4}"'.format(record, lines, filename, tablename, difference))


def handle(event, context):
    dbconn = connect()
    create_table(dbconn=dbconn, tablename=args.table)
    if args.pipe_delimited:
        import_pipe_delimited_data(
            dbconn=dbconn,
            tablename=args.table, 
            filename=args.filename
            )
    else:
        import_csv_delimited_data(
            dbconn=dbconn,
            tablename=args.table,
            filename=args.filename
            )


if __name__ == '__main__':
    event = {}
    context = {}
    handle(event, context)