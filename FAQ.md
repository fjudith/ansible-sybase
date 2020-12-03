# Frequently Asked Questions

## Why leveraging Cloud-Init ?

Cloud-Init is a portable standard to unify the delivery of pre-configured machines.
They can easyly be reused accross cloud service provider specific distributions and are reliable for dependency installation like  

## Vagrant boxes

### Why a Scripted and Ansible deployments ?

The `scripted` deployment is close to the SAP [Installation Guide For Linux](https://help.sap.com/viewer/244b731a316a4de0ad1dd618937b0f8e/16.0.0.0/en-US), where the `ansible` is more **robust** transcript. Following the moto _Automate what you know to run manually_, change are first released to the `scripted` deployment method, then capitalized to `ansible`.

> The scripted method is also easier to **containerize** using the Dockerfile specification.

## Why leveraging ansible_local provisionner ?

The [Vagrantfile](./Vagrantfile) leverage the [ansible_local](https://www.vagrantup.com/docs/provisioning/ansible_local) provisionner to resolve the issue where [Vagrant](https://www.vagrantup.com) is supported by the Developper workstation but not [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#control-node-requirements), which noticeably the case for **Microsoft Windows**.

> The `ansible_local` has a performance penalty with respect to the `ansible` _(remote)_ provisionner, because Vagrant will require to synchronise the repository and install the required dependencies to run Ansible locally.

### Benchmark

The following benchmark evaluates Vagrant build time between the [Official](https://app.vagrantup.com/centos/boxes/7) centos box and the one maintained by [Hashicorp](https://app.vagrantup.com/generic/boxes/centos7).
The build time has been evaluated 3 time for each box flavor, using the [Scripted](./hack/vagrant/boxes-scripted.example) and [Ansible](./hack/vagrant/boxes-ansible.example)

**Bastion**

Machine type            | box             | version | Antivirus | linked clone | Sybase deployment | build time
------------------------|-----------------|---------|-----------|--------------|---------------------|-----------
Bastion (1 cpu/ 1024MB) | generic/centos7 | 3.1.8   | off       | false        | scripted            | 00:10:00
Bastion (1 cpu/ 1024MB) | centos/7        | 3004.1  | off       | false        | scripted            | 00:11:00
Bastion (1 cpu/ 1024MB) | generic/centos7 | 3.1.8   | off       | false        | Ansible             | 00:10:00
Bastion (1 cpu/ 1024MB) | centos/7        | 3004.1  | off       | false        | Ansible             | 00:11:00

#### Vagrant generic/centos7 box

**filesystem layout (bastion)**:

```text
Filesystem                       Size  Used Avail Use% Mounted on
devtmpfs                         485M     0  485M   0% /dev
tmpfs                            496M     0  496M   0% /dev/shm
tmpfs                            496M   13M  483M   3% /run
tmpfs                            496M     0  496M   0% /sys/fs/cgroup
/dev/mapper/centos_centos7-root   50G  2.2G   48G   5% /
/dev/mapper/centos_centos7-home   75G  876M   75G   2% /home
/dev/sda1                       1014M  131M  884M  13% /boot
tmpfs                            100M     0  100M   0% /run/user/1000
```

#### Official Centos centos/7 box

**Filesystem layout (bastion)**:

```text
Filesystem      Size  Used Avail Use% Mounted on
devtmpfs        489M     0  489M   0% /dev
tmpfs           496M     0  496M   0% /dev/shm
tmpfs           496M  6.8M  489M   2% /run
tmpfs           496M     0  496M   0% /sys/fs/cgroup
/dev/sda1        40G  6.9G   34G  18% /
tmpfs           100M     0  100M   0% /run/user/0
tmpfs           100M     0  100M   0% /run/user/1000
```