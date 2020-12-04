# Ansible-Sybase hack guidelines

This document describes how you can use the scripts from the `hack` directory and gives a brief introduction and explanation of these scripts.

## Overview

the `hack` directory contains many scripts that ensure continuous development of the project, enhance the robustness of the code, improve development efficiency, etc. The explanations and descriptions of the scripts are helpful for contributors. For details, refer to the following guidelines.

# Key scripts

* [`hack/local-up-vagrant.sh`](./local-up-vagrant.sh): This script boots a Virtualbox local environment running a **bastion server** that includes the SAP Open Client (OCS) and a **database** server running SAP Adaptive Server Enterprise (ASE) Developer Edition.
* [`hack/provision.sh`](./provision.sh): This script forces the synchronization the repository inside all VMs, update Cloud-Init configuration files, and rerun the playbook located in the [./vagrant](./vagrant) directory, in the case of a general update of the code base.
* [`hack/provision-bastion.sh`](./provision-bastion.sh): This script achieve similar task of [`hack/provision.sh`](./provision.sh). But specifically aims `bastion` hosts. Run this script in the case of SAP OCS Bastion specific updates of the code base.
* [`hack/provision-database.sh`](./provision-database.sh): This script achieve similar task of [`hack/provision.sh`](./provision.sh). But specifically aims `database` hosts. Run this script in the case of SAP ASE Database specific updates of the code base.
v