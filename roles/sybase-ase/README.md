# Sybase-ASE

Ansible role for install SAP Adaptive Server Enterprise (ASE) server.

Default installation directories:

**Binaries**: `/home/sybase`
**Data**: `/home/sybase`

## Example playbook

```yaml
- hosts: dbservers
  roles:
    - sybase-ase
```