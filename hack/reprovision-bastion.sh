#!/usr/bin/env bash

# https://www.vagrantup.com/docs/other/wsl.html
export VAGRANT_WSL_ENABLE_WINDOWS_ACCESS="1"

time vagrant rsync bastion && \
time vagrant up --provision bastion