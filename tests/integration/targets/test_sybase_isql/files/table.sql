if not exists (
    select 1
    from sysobjects
    where name = 'fakenames'
    and type = 'U'
)
  execute('
    CREATE TABLE fakenames (
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
    )'
  )
else
  print "Table 'fakenames' already exists in database"
go