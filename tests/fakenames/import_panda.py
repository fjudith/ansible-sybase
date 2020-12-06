import os
import argparse
import logging
import pyodbc
import pandas as pd
from collections import OrderedDict

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
parser.add_argument('-D', '--database', help='taget SQL database', default=os.environ.get('FK_DATBASE', default="cidb"))
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
        

def import_csv_delimited_data(dbconn, tablename, filename, delimiter):
    logger.info('Load CSV data from file "{0}" to table "{1}"'.format(filename, tablename))
    
    # Table configuration
    cursor = dbconn.cursor()
    cursor.execute('SET IDENTITY_INSERT {0} ON'.format(tablename))
    cursor.commit()

    # Import data
    reader = pd.read_csv(filepath_or_buffer=filename, encoding='utf-8-sig', sep=delimiter)
    df = pd.DataFrame(data=reader)
    
    # Fix convertion
    df['CCNumber'] = df['CCNumber'].astype(str)
    df['WesternUnionMTCN'] = df['WesternUnionMTCN'].astype(str)
    df['CVV2'] = df['CVV2'].astype(str)
    df['MoneyGramMTCN'] = df['MoneyGramMTCN'].astype(str)
    df['ZipCode'] = df['ZipCode'].astype(str)
    df['City'] = df['City'].str.replace('Ÿ','Y')
    df['Password'] = df['Password'].str.replace('œ','oe')
    df['Company'] = df['Company'].fillna('n/a')

    # Prepare query
    query = 'insert into ' + tablename + '({0}) values ({1})'
    query = query.format(','.join(df.columns.values), ','.join('?' * df.columns.size)).lower()
    
    # Fit to database fields
    field_transform = {
        'mothersmaiden': 'maidenname',
        'ups': 'upstracking'
    }
    for key,value in field_transform.items():
        query = query.replace(key, value)

    amount_of_lines = df.values.shape[0]
    logger.info('Processing "{0}" lines'.format(amount_of_lines))
    amount_of_records = 0
    
    for data in df.itertuples():
        cursor = dbconn.cursor()

        cursor.execute(query, [
            data.Number, data.Gender, data.NameSet, data.Title, data.GivenName, data.MiddleInitial, data.Surname, data.StreetAddress, data.City, 
            data.State, data.StateFull, data.ZipCode, data.Country, data.CountryFull, data.EmailAddress, data.Username, data.Password, data.BrowserUserAgent, data.TelephoneNumber, 
            data.TelephoneCountryCode, data.MothersMaiden, data.Birthday, data.Age, data.TropicalZodiac, data.CCType, data.CCNumber, data.CVV2, data.CCExpires, data.NationalID, 
            data.UPS, data.WesternUnionMTCN, data.MoneyGramMTCN, data.Color, data.Occupation, data.Company, data.Vehicle, data.Domain, data.BloodType, data.Pounds, 
            data.Kilograms, data.FeetInches, data.Centimeters, data.GUID, data.Latitude, data.Longitude
            ]
        )
        cursor.commit()
        amount_of_records += 1

    logger.info('Imported {0}/{1} line from file "{2}" to table "{3}"'.format(amount_of_records, amount_of_lines, filename, tablename))


def handle(event, context):
    dbconn = connect()
    create_table(dbconn=dbconn, tablename=args.table)
    if args.pipe_delimited:
        import_csv_delimited_data(
            dbconn=dbconn,
            tablename=args.table, 
            filename=args.filename,
            delimiter='|'
            )
    else:
        import_csv_delimited_data(
            dbconn=dbconn,
            tablename=args.table,
            filename=args.filename,
            delimiter=','
            )


if __name__ == '__main__':
    event = {}
    context = {}
    handle(event, context)