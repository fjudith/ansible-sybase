# ROADMAP

## v1.0.0

### Local development environment

This stream relates to the delivery located in the [./hack/](./hack)

* [ ] Run local Sybase ASE server instances using Vagrant
* [x] Run local Sybase OCS client instances using Vagrant
* [x] Leverage Cloud-Init for instance initialization
* [x] Ensure compatibility with Virtualbox
* [ ] Ensure comptability with Hyper-V

### Sybase installation for Linux

This stream relates to the delivery located in the following directories:

* [./roles/sybase-ase](./roles/sybase-ase/)
* [./roles/sybase-ocs](./roles/sybase-ocs/)
* [./roles/liquibase](./roles/liquibase/)
  
* [ ] Manage SAP ASE server installation using Ansible
* [x] Manage SAP OCS client installation using Ansible
* [x] Manage [Liquibase](http://liquibase.org) client installation using Ansible
* [x] Manage Docker-CE engine installation on OCS client instance
