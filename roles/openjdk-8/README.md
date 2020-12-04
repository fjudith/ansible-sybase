# Oracle-JDK8

Ansible role for installing Oracle Java 8 JDK.

Java is installed to: `/usr/share/java-1.8.0`

Java alternatives are updated to use this by default and executable is
`/usr/bin/java`.

## Role Variables

```yaml
java:
  version: 1.8.0_211
  install:
    archive: jdk-8u211-linux-x64.tar.gz
    url: 'https://download.oracle.com/otn/java/jdk/8u211-b12/478a62b7d4e34b78b671c754eaaf38ab/{{ java_archive_name }}'
    directory: /usr/share/java-1.8.0
```

## Example Playbook

```yaml
    - hosts: servers
      roles:
         - oracle-jdk8
```
