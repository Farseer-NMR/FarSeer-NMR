#!/bin/bash

# https://stackoverflow.com/questions/7066625/how-to-find-the-linux-processor-chip-architecture
architecture=$(lscpu | grep Architecture)

# https://stackoverflow.com/questions/10586153/split-string-into-an-array-in-bash
read -r -a array <<< "$architecture"
arch="${array[1]}"
bit32="i686"
bit64="x86_64"

#echo "${array[1]}"

if [ "$arch" == "$bit64" ]
then
    spec="spec-file_64bit.txt"
    echo "Found 64-bit architecture..."
fi

if [ "$arch" == "$bit32" ]
then
    spec="spec-file_32bit.txt"
    echo "Found 32-bit architecture..."
fi

specfile="$(pwd)/Documentation/${spec}"

conda create --name farseernmr --file $specfile

tee run_farseer.sh <<< \
'#!/usr/bin/env bash

export FARSEER_ROOT="$(pwd)"
export PYTHONPATH=$PYTHONPATH:${FARSEER_ROOT}

source activate farseernmr

python $FARSEER_ROOT/main.py $*
'

chmod u+x run_farseer.sh

echo \
"   *****
    
    Farseer-NMR as been correctly configured and
    
    TO LAUNCH FARSEER-NMR:
    
    ./run_farseer.sh
    
    :-)
"
