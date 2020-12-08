#!/usr/bin/env bash

ansible-test integration --docker -v --color --retry-on-error --continue-on-error --python 3.6 --diff --coverage