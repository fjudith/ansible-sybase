#!/usr/bin/env bash

# Retries a command on failure.
# $1 - the max number of attempts
# $2... - the command to run
retry() {
    local -r -i max_attempts="$1"; shift
    local -r cmd="$@"
    local -i attempt_num=1

    until $cmd
    do
        if (( attempt_num == max_attempts ))
        then
            echo "Attempt $attempt_num failed and there are no more attempts left!"
            return 1
        else
            echo "Attempt $attempt_num failed! Trying again in $attempt_num seconds..."
            sleep $(( attempt_num++ ))
        fi
    done
}

docker-compose -f hack/docker/docker-compose.yaml pull
docker-compose -f hack/docker/docker-compose.yaml up --detach

echo "Wait for Sysbase listen port"
retry 30 nc -vz localhost 5000 > /dev/null 2>&1

echo "Wait for Sybase master database creation"
retry 30 docker exec sybase isql -U sa -P myPassword -S MYSYBASE -D master > /dev/null 2>&1


echo "Wait for Sybase master database initialization"
STATUS=$(docker exec -i sybase bash -c 'grep "Finished initialization." ${SYBASE}/ASE-16_0/install/MYSYBASE.log | wc -c')
until [[ ${STATUS} -gt 400 ]]
do
    STATUS=$(docker exec -i sybase bash -c 'grep "Finished initialization." ${SYBASE}/ASE-16_0/install/MYSYBASE.log | wc -c')
    printf "." && sleep 5
done
echo ""

echo "Run Ansible tests"
ansible-test integration \
--docker "quay.io/ansible/default-test-container:2.9.0" \
--docker-network "docker_sybase" \
--python "3.6" \
-vvv --color --continue-on-error --diff --coverage
# ansible-test integration \
# --docker "docker.io/sqlops/sybase-test-container:1.0.0-centos7" \
# --docker-network "docker_sybase" \
# --python "3.6" \
# -v --color --continue-on-error --diff --coverage