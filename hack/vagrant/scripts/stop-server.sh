#!/bin/bash

[ $# -ne 1 ] && echo "Usage: $0 <SYB_SERVER>" && exit 1

_server=${1}

source /home/sybase/SYBASE.sh

_isql=${SYBROOT}/${SYBASE_OCS}/bin/isql

if [ -x ${_isql} ]
then
  echo "Stopping Sybase server .... ${_server}"
  ${_isql} -U sa -S ${_server} << EOF
$( cat /home/sybase/.sa_password )
shutdown
go
EOF
fi