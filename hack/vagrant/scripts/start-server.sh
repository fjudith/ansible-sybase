#!/bin/sh

[ $# -ne 1 ] && echo "Usage: $0 <SYB_SERVER>" && exit 1
_server=${1}
. /home/sybase/SYBASE.sh
_run_file=${SYBROOT}/${SYBASE_ASE}/install/RUN_${_server}
if [ -x ${_run_file} ]
then
        echo "Starting Sybase server ... ${_server}"
        . ${_run_file}
else
        echo "Cannot find run file ${_run_server}"
        exit 1
fi