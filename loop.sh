#!/bin/bash

# Command example :
# bash loop.sh -snapshot 154 -ratio_number 1 -bg 1 -rotation_key 0 res_unres_sn 0

#pth="./data/SILCC_hdf5_plt_cnt_0"

#for a test run:
pth="./gas_temp.npy"

#if you want to post-proc. a few files
#counter=154
#while [ $counter -le 200]

# Get all parameters from input
while [[ $# -gt 0 ]]; do
    case "$1" in
    -snapshot)
        snapshot=$2
        shift
        ;;
    -ratio_number)
    	ratio_number=$2
    	shift
        ;;
    -bg)
    	bg=$2
    	shift
        ;;
    -rotation_key)
        rotation_key=$2
        shift
        ;;
    -res_unres_sn)
        res_unres_sn=$2
        shift
        ;;
    *)
        echo "Invalid argument: $1"
        exit 1
    esac
    shift
done

if [ ${param} ]; then
    echo 'snapshot ration_number gb rotation_key res_unres_sn'
    exit 1;
fi

# Verify if all parameters are given
if [ -z ${snapshot+x} ]; then echo "No snapshot number given !"; exit; fi
if [ -z ${ratio_number+x} ]; then echo "The emission line ratio was not specified !"; exit; fi
if [ -z ${bg+x} ]; then echo "No background parameter given !"; exit; fi
if [ -z ${rotation_key+x} ]; then echo "No rotation_key given !"; exit; fi
if [ -z ${res_unres_sn+x} ]; then echo "Not specified: resolved or unresolved SN calculations !"; exit; fi

echo 'Starting the emission calculations...'

if [ $bg == 0 ] 
then 
	python emiss_3Dcube.py <<< $counter $ratio_number $bg $rotation_key
fi

if [ $bg == 1 ] 
then 
	python emiss_3Dcube.py <<< $counter $ratio_number $bg $rotation_key
	bg=$(( $bg - 1 ))
	if (( $bg == 0 )) 
	then
		python emiss_3Dcube.py <<< $counter $ratio_number $bg $rotation_key
	fi
fi

echo 'Tau calculations...'
python tau.py <<< $ratio_number $rotation_key
echo 'RT calculations...'
python rt.py <<< $rotation_key $bg $res_unres_sn

echo All done