# Vagrant Development Environment

* **Bastion**: Host running Sybase Open Client
* **Database**: Host running SAP Adaptive Enterprise 16.0

## Ansible local provisionner

The Vagrant environment leverage the Ansible Local provisionner which depends on the playbooks located in the [hack/vagrant/sync/folder](./synced)

## Users of Windows Subsystem For Linux

To make Vagrant works with Windows Subsystem for Linux, it is required to align versions installed on Windows and WSL distro.
Then the `VAGRANT_WSL_ENABLE_WINDOWS_ACCESS="1"` environment variable have to be added to the `/etc/environment` file.

```bash
export VAGRANT_WSL_ENABLE_WINDOWS_ACCESS="1"
echo VAGRANT_WSL_ENABLE_WINDOWS_ACCESS="1" | sudo tee -a /etc/environment
```
