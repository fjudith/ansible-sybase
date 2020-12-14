#!/usr/bin/env bash

ansible-test integration \
--docker "docker.io/sqlops/sybase-test-container:1.0.0-centos7" \
--docker-network "docker_sybase" \
--python "2.7" \
-v --color --continue-on-error --diff --coverage