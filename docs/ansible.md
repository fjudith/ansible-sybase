# Ansible
## Test guidelines

The tests are leveraging [Ansible Collections Testing guideline]
## Mudules local testing

To test modules locally the operator must run [Ansible](https://ansible.com) and [Docker](https://docker.com) on its personnal computer.
Redhat/Centos and Debian/Ubuntu distributions are supported, as well as [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10) if running on Microsoft Windows.

### Start Sybase server using Docker

A Sybase instance is required to run the tests. Run the following script to:

1. Download the Sybase container image.
2. Create a dedicated `docker_sybase` network for both Sybase and Ansible-Test containers.
3. Run the Sybase container.

```bash
hack/local-test-docker.sh
```

```text
Pulling sybase ... done
Starting sybase ... done
Wait for Sysbase listen port
Wait for Sybase master database creation
Wait for Sybase master database initialization

Run Ansible tests
...
```