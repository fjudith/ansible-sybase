#!/usr/bin/env bash
export VAGRANT_WSL_ENABLE_WINDOWS_ACCESS="1"

vagrant plugin install vagrant-scp && \
vagrant plugin install vagrant-hostmanager && \
vagrant up