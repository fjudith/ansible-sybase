#!/usr/bin/env bash

set -e

export SYBASE="/home/sybase"

export PATH=${PATH}:${SYBASE}/ASE-16_0/bin/:${SYBASE}/OCS-16_0/bin

# cp /tmp/sysctl.conf /etc/sysctl.conf && \
# /sbin/sysctl -p

# libaio
# echo "Install libaio" && \
# curl -OLS http://mirror.centos.org/centos/7/os/x86_64/Packages/libaio-0.3.109-13.el7.x86_64.rpm && \
# rpm -ivh --nodeps libaio-0.3.109-13.el7.x86_64.rpm

# gtk2
# echo "Install gtk2" && \
# curl -OLS http://mirror.centos.org/centos/7/os/x86_64/Packages/gtk2-2.24.31-1.el7.x86_64.rpm && \
# rpm -ivh --nodeps gtk2-2.24.31-1.el7.x86_64.rpm

# glibc
# echo "install glibc"
# curl -OLS ftp://ftp.pbone.net/mirror/ftp.scientificlinux.org/linux/scientific/7.2/x86_64/os/Packages/glibc-2.17-105.el7.i686.rpm && \
# rpm -Uvh --oldpackage --nodeps glibc-2.17-105.el7.i686.rpm

# Unpack Sybase Developer Edition
if [[ -f /tmp/ASE_Suite.linuxamd64.tgz ]];
then
    echo "SAP ASE package already provisionned in '/tmp'"
else
    echo "SAP ASE package not found in '/tmp'. Downloading..."
    curl -o /tmp/ASE_Suite.linuxamd64.tgz -LS http://repository.transtep.com/repository/thirdparty/sybase/ASE16SP02/ASE_Suite.linuxamd64.tgz
fi
echo "Unpacking SAP ASE package..." && \
mkdir -p /tmp/ && \
tar xfz /tmp/ASE_Suite.linuxamd64.tgz -C /tmp/ && \
rm -rf /tmp/ASE_Suite.linuxamd64.tgz

# Install Sybase Open Client and librairies
echo "Install SAP OCS" && \
chown -R sybase:sybase ${SYBASE}/ && \
echo "source ${SYBASE}/SYBASE.sh" | tee -a ${SYBASE}/.bashrc && \
/tmp/ASE_Suite/setup.bin -f /tmp/sybase-ocs-response.conf \
-i silent \
-DAGREE_TO_SAP_LICENSE=true \
-DRUN_SILENT=true

# Remove ASE installation files
rm -vrf /tmp/ASE_Suite