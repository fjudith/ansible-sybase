#!/usr/bin/env bash

ansible-test integration \
--docker "quay.io/ansible/default-test-container:2.9.0" \
--docker-network "docker_sybase" \
--python "3.6" \
-v --color --continue-on-error --diff --coverage