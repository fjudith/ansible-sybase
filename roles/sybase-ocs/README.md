# Sybase-OCS

Ansible role for install SAP Open Client (OCS) client.

Default installation directories:

**Binaries**: `/home/sybase`

## Example playbook

```yaml
- hosts: bastions
  roles:
    - sybase-ocs
```