# How-to: Vagrant

The following how-to describes how to run the [Vagrant](http://vagrantup.com) local environment which includes a bastion server with Open Client (OCS) installed and a database server running SAP Adaptive Server (ASE).

## Pre-requisits

* [ ] [Vagrant 2.2.x](https://vagrantup.com)
* [ ] [Virtualbox v6.1.x](https://www.virtualbox.org)
* [ ] _Windows only_ : [Git for Windows](https://gitforwindows.org)
* [ ] Sybase installation package*

> **Warning**:
> The Sybase installation package is not provided in the repository.
> It is recommanded to use the SAP ASE Developper Edition that you can get from the SAP Portal.
> The tarball have to be copied manually under the `hack/vagrant/packages`, and named as `ASE_Suite.linuxamd64.tgz`.

There is no dependancy to with [Ansible](https://www.ansible.com) because the Vagrant description file leverages the [`ansible_local`](https://www.vagrantup.com/docs/provisioning/ansible_local) provisionner.

## Quickstart

Once the repository cloned locally, run the following command to build and and start the bastion and database servers.

```bash
vagrant up
```

## End-to-End test

the [`hack`](../hack/) directory contains the [`local-up-vagrant.sh`](../hack/local-up-vagrant.sh) scripts which run the vagrant environment as well as to Ansible playbooks to test Sybase basic operations.

Once the repository clone locally, run the following command to perform end-to-end tests.

```bash
hack/local-up-vagrant.sh
```
