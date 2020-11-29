#!/usr/bin/env bash

set -e

SA_PASSWORD=${SA_PASSWORD:="myPassword"}

export SYBASE="/home/sybase"

export PATH=${PATH}:${SYBASE}/ASE-16_0/bin/:${SYBASE}/OCS-16_0/bin

cp /tmp/sysctl.conf /etc/sysctl.conf && \
/sbin/sysctl -p

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

# Install Sybase
echo "Install SAP ASE" && \
/tmp/ASE_Suite/setup.bin -f /tmp/sybase-ase-response.conf \
-i silent \
-DAGREE_TO_SAP_LICENSE=true \
-DRUN_SILENT=true

# Copy resource file
echo "Replace resource file" && \
cp /tmp/sybase-ase.rs ${SYBASE}/ASE-16_0/sybase-ase.rs

# Build ASE server
echo "Build MYSYBASE server" && \
source ${SYBASE}/SYBASE.sh && \
${SYBASE}/ASE-16_0/bin/srvbuildres -r ${SYBASE}/ASE-16_0/sybase-ase.rs

# Change the Sybase interface
echo "Update SAP ASE  listen interfaces" && \
mv ${SYBASE}/interfaces ${SYBASE}/interfaces.backup && \
cp /tmp/interfaces ${SYBASE}/

# Set the Sybase start/stop scripts
echo "Install stop/start scripts" && \
mkdir -p ${SYBASE}/bin && \
cp /tmp/start-server.sh ${SYBASE}/bin/ && \
chmod +x ${SYBASE}/bin/start-server.sh && \
cp /tmp/stop-server.sh ${SYBASE}/bin/ && \
chmod +x ${SYBASE}/bin/stop-server.sh && \

# Kill running processes
sudo /usr/bin/pkill --echo dataserver

# Enable Sybase Service
echo "Install systemd service"
echo "myPassword" | tee ${SYBASE}/.sa_password && \
echo "source ${SYBASE}/SYBASE.sh" | tee -a ${SYBASE}/.bashrc && \
chown -R sybase:sybase ${SYBASE}/ && \
cp /tmp/sybase.service /etc/systemd/system/sybase.service && \
systemctl enable sybase.service && \
systemctl start sybase.service

# Stop password

# Remove ASE installation files
rm -vrf /tmp/ASE_Suite