# Ansible-Sybase

[![Plugins CI](https://github.com/fjudith/ansible-sybase/workflows/Plugins%20CI/badge.svg?event=push)](https://github.com/fjudith/ansible-sybase/actions?query=workflow%3A"Plugins+CI") [![Roles CI](https://github.com/fjudith/ansible-sybase/workflows/Roles%20CI/badge.svg?event=push)](https://github.com/fjudith/ansible-sybase/actions?query=workflow%3A"Roles+CI") [![Codecov](https://img.shields.io/codecov/c/github/fjudith/ansible-sybase)](https://codecov.io/gh/fjudith/ansible-sybase)

## Included content

- **Modules**:
  - [sybase_user](./plugins/modules)
  - [sybase_db](./plugins/modules)
  - [sybase_query](./plugins/modules)

- **Roles**:
  - [sybase-ase](./roles/sybase-ase)
  - [sybase-ocs](./roles/sybase-ocs)
  - [liquidbase](./roles/liquidbase)
  - [openjdk-8](./role/openjdk-8)
  - [common-firewall (vagrant only)](./roles/common-firewall)

## Tested with Ansible

- 2.9

This repository contains an Ansible playbook to acheive the following operations:

* [x] Enable local development environment
* [x] Manage SAP ASE and OCS installation on Redhat/Centos distributions using Ansible
* [ ] _In progress_ : Manage basic Database Administrator related operations (database, table, permissions, backup & restore, etc.) using Ansible
* [ ] _In progress_ : Manage basic Database Developer related operations (stored procedure compilation) using Ansible

Please refer to the [ROADMAP](./ROADMAP.md) for more details on the progress

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
* [Powershell Core](https://github.com/powershell/powershell): Language used for Windows specific shell scripting