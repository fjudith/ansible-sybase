use master
go
disk resize name='master', size='200m'
go
create database 'fakenames' on master = '50m'
go
exec sp_extendsegment 'logsegment', 'fakenames', 'master'
go
create login 'fakenames' with password 'fakenames'
go
exec sp_dboption 'fakenames', 'abort tran on log full', true
go
exec sp_dboption 'fakenames', 'allow nulls by default', true
go
exec sp_dboption 'fakenames', 'ddl in tran', true
go
exec sp_dboption 'fakenames', 'trunc log on chkpt', true
go
exec sp_dboption 'fakenames', 'full logging for select into', true
go
exec sp_dboption 'fakenames', 'full logging for alter table', true
go

use fakenames
sp_dboption 'fakenames', 'select into', true
go