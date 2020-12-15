use master
go
disk resize name='master', size='200m'
go
create database 'fakenames' on master = '50m'
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
exec sp_dboption 'fakenames', 'select into', true
go

-- Generates Error: This command has been ignored.  Extending the log segment on device 'master'", "would leave no space for creating objects in database 'fk_shell'.
-- https://help.sap.com/viewer/29a04b8081884fb5b715fe4aa1ab4ad2/16.0.2.9/en-US/ab667031bc2b10148eb1d029c4f988ca.html?q=sp_extendsegment
-- exec sp_dboption fakenames, 'single user', true
-- go

-- use fakenames
-- go
-- exec sp_extendsegment 'logsegment', 'fakenames', 'master'
-- go
