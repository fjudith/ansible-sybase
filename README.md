# Ansible-Sybase

[![Plugins CI](https://github.com/fjudith/ansible-sybase/actions/workflows/ansible-test-plugins.yaml/badge.svg)](https://github.com/fjudith/ansible-sybase/actions/workflows/ansible-test-plugins.yaml) [![Roles CI](https://github.com/fjudith/ansible-sybase/actions/workflows/ansible-test-roles.yaml/badge.svg)](https://github.com/fjudith/ansible-sybase/actions/workflows/ansible-test-roles.yaml) [![Codecov](https://img.shields.io/codecov/c/github/fjudith/ansible-sybase)](https://codecov.io/gh/fjudith/ansible-sybase)

## Included content

- **Modules**:
  - [sybase_db](./plugins/modules): Database import/export using `bcp` wrapper, and removal/simple creation using `pyodbc` and `FreeTDS` python drivers.
  - [sybase_isql](./plugins/modules): Run SQL scripts using `isql64` or `isql` command wrapper.
  - [sybase_query](./plugins/modules): Run SQL queries using `pyodbc` and `FreeTDS` python drivers.

- **Roles**:
  - [sybase-ase](./roles/sybase-ase): Install SAP Adaptive Server Enterprise (ASE / Sybase) server
  - [sybase-ocs](./roles/sybase-ocs): Install SAP OpenClient (OCS) client
  - [liquidbase](./roles/liquidbase): Install Liquidbase database development tool
  - [openjdk-8](./role/openjdk-8): Install AdoptOpenJDK 8 (required for `roles/liquidbase`)
  - [common-firewall (vagrant only)](./roles/common-firewall): Manage firewalld (Required for `roles\sybase-ase`)

## Cloning

This repository is designed as per [Ansible Collections]() guidelines. It therere required to clone this repository in a specific directory structure.

```bash
mdkdir -p ansible_collections/sqlops/ && \
cd ansible_collections/sqlops/ && \
git clone "https://github.com/fjudith/ansible-sybase" sybase
```

## Tested with Ansible

- 2.9.x: Centos 7, Ubuntu Bionic (18.04 LTS), Ubuntu Focal (20.04 LTS)
- 2.10.x: : Centos 7, Ubuntu Bionic (18.04 LTS), Ubuntu Focal (20.04 LTS)

## Roadmap

Please refer to the [ROADMAP](./ROADMAP.md) for more details on the progress.

## Technologies

* [Vagrant](https://www.vagrantup.com): Local development environment provisionning
* [Cloud-Init](https://cloud-init.io): Initial instance bootime provisionning
* [Ansible](https://www.ansible.com): Software provisionning and configuration management
* [Liquibase](https://liquibase.org): Database operation management

## Languages

* [Ansible](https://www.ansible.com): YAML based Domain-specific language (DSL) for configuration management
* [Ansible-Lint](https://github.com/ansible/ansible-lint): Code style compliance processor
* [Bash](https://fr.wikipedia.org/wiki/Bourne-Again_shell): Language used for general shell scripting
* [Python](https://python.org): Language used to write unit tests and Ansible modules
* [PyODBC](https://github.com/mkleehammer/pyodbc/wiki): Open source Python module that makes accessing ODBC databases simple
* [Powershell Core](https://github.com/powershell/powershell): Language used for Windows specific shell scripting (ref. [hack](./hack))
