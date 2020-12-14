# Ansible-Sybase

[![Plugins CI](https://github.com/fjudith/ansible-sybase/workflows/Plugins%20CI/badge.svg?event=push)](https://github.com/fjudith/ansible-sybase/actions?query=workflow%3A"Plugins+CI") [![Roles CI](https://github.com/fjudith/ansible-sybase/workflows/Roles%20CI/badge.svg?event=push)](https://github.com/fjudith/ansible-sybase/actions?query=workflow%3A"Roles+CI") [![Codecov](https://img.shields.io/codecov/c/github/fjudith/ansible-sybase)](https://codecov.io/gh/fjudith/ansible-sybase)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Ffjudith%2Fansible-sybase.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Ffjudith%2Fansible-sybase?ref=badge_shield)

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

## Cloning

This repository is designed as per [Ansible Collections]() guidelines. It therere required to clone this repository in a specific directory structure.

```bash
mdkdir -p ansible_collections/sqlops/ && \
cd ansible_collections/sqlops/ && \
git clone "https://github.com/fjudith/ansible-sybase" sybase
```

## Tested with Ansible

- 2.9.x
- 2.10.x

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
* [Powershell Core](https://github.com/powershell/powershell): Language used for Windows specific shell scripting

## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Ffjudith%2Fansible-sybase.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Ffjudith%2Fansible-sybase?ref=badge_large)