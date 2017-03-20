#! /bin/bash

signtype=$1
installpath=$2
filepath=$3


apks=`awk -F " " -v var1=${signtype} -v var2=${installpath} '{if($2 == var1 && $3 == var2){print $1}}' $filepath/apk_sign.txt`

apk_list="$apks"

echo $apk_list
