# Ansible-Sybase hack guidelines

This document describes how you can use the scripts from the `hack` directory and gives a brief introduction and explanation of these scripts.

## Overview

the `hack` directory contains many scripts that ensure continuous development of the project, enhance the robustness of the code, improve development efficiency, etc. The explanations and descriptions of the scripts are helpful for contributors. For details, refer to the following guidelines.

# Key scripts

* [`local-up-vagrant.sh`](./hack/local-up-vagrant.sh): This script boots a Virtualbox local environment running a **bastion server** that includes the SAP Open Client (OSE) and a **database** server running SAP Adaptive Server Enterprise (ASE) Developer Edition.
