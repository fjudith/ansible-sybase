#!/usr/bin/env bash

set -e

export SYBASE="/opt/sybase"

export PATH=${PATH}:${SYBASE}/ASE-16_0/bin/:${SYBASE}/OCS-16_0/bin

cp /tmp/sysctl.conf /etc/sysctl.conf && \
/sbin/sysctl -p

# libaio
curl -OLS http://mirror.centos.org/centos/7/os/x86_64/Packages/libaio-0.3.109-13.el7.x86_64.rpm && \
rpm -ivh --nodeps libaio-0.3.109-13.el7.x86_64.rpm

# gtk2
curl -OLS http://mirror.centos.org/centos/7/os/x86_64/Packages/gtk2-2.24.31-1.el7.x86_64.rpm && \
rpm -ivh --nodeps gtk2-2.24.31-1.el7.x86_64.rpm

# glibc
# curl -OLS ftp://ftp.pbone.net/mirror/ftp.scientificlinux.org/linux/scientific/7.2/x86_64/os/Packages/glibc-2.17-105.el7.i686.rpm && \
# rpm -Uvh --oldpackage --nodeps glibc-2.17-105.el7.i686.rpm

# Download Sybase Developer Edition
if [! -f /tmp/ASE_Suite.linuxamd64.tgz ];
then
    curl -o /tmp/ASE_Suite.linuxamd64.tgz -LS http://repository.transtep.com/repository/thirdparty/sybase/ASE16SP02/ASE_Suite.linuxamd64.tgz
fi
mkdir -p /tmp/ && \
tar xfz /tmp/ASE_Suite.linuxamd64.tgz -C /tmp/ && \
rm -rf /tmp/ASE_Suite.linuxamd64.tgz

# Install Sybase
/tmp/ASE_Suite/setup.bin -f /tmp/sybase-response.conf \
-i silent \
-DAGREE_TO_SAP_LICENSE=true \
-DRUN_SILENT=true

# Copy resource file
cp /tmp/sybase-ase.rs ${SYBASE}/ASE-16_0/sybase-ase.rs

# Build ASE server
source ${SYBASE}/SYBASE.sh && \
${SYBASE}/ASE-16_0/bin/srvbuildres -r ${SYBASE}/ASE-16_0/sybase-ase.rs

# Change the Sybase interface
# Set the Sybase startup script in entrypoint.sh
mv ${SYBASE}/interfaces ${SYBASE}/interfaces.backup && \
cp /tmp/interfaces ${SYBASE}/ && \
cp /tmp/start-sybase.sh /usr/local/bin/ && \
chmod +x /usr/local/bin/start-sybase.sh