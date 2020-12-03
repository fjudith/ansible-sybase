# Troubleshooting


## Ansible: Monitor SAP ASE installation

Ansible does not return the stdout in realtime, it is therefore necessary to monitor logs inside the database instance

> The following guide lines leverage Vagrant.
> For remote Cloud/On-premise instances, use the appropriate `ssh` command

```bash
vagrant ssh database
```

**SAP ASE/OCS Installation**:

```bash
sudo cat /home/sybase/log/ASE_Suite.log
```

**SAP ASE initial database creation**

```bash
sudo cat /home/sybase/ASE-16_0/install/MYSYBASE.log
```
