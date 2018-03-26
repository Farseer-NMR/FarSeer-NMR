#!/bin/bash

echo "Checking there is sufficient space for installation"
FREE_SPACE=`df -H "$PWD" | awk '{print $4'} | cut -d'G' -f1`

if [[$FREE_SPACE -lt 3 ]]; then
    echo "Less than 3GB free space, cannot install Miniconda, stopping"
    exit 1
fi

spec32="spec-file_32bit.txt"
spec64="spec-file_64bit.txt"

# https://stackoverflow.com/questions/7066625/how-to-find-the-linux-processor-chip-architecture
architecture=$(lscpu | grep Architecture)

echo "*** Reading computer's architecture..."
# https://stackoverflow.com/questions/10586153/split-string-into-an-array-in-bash
read -r -a array <<< "$architecture"
arch="${array[1]}"
bit32="i686"
bit64="x86_64"

function queryuser {
    echo \
"*** Farseer-NMR could not detect your computer's architecture.
*** Please select one of the following options:
*** (1) 64-bit (2) 32-bit: "; read OPTION
}

#echo "${array[1]}"

if [ $arch == $bit64 ]; then
    spec=$spec64
    echo "*** Found 64-bit architecture!"
    echo

elif [ $arch == $bit32 ]; then
    spec=$spec32
    echo "*** Found 32-bit architecture!"
    echo
else
    OPTION="99"
    while [ $OPTION != "1" -a  $OPTION != "2" ]; do
        queryuser
    done
    
    if [ $OPTION == "1" ]; then
        spec=$spec64
        CHOICE="64"
    elif [ $OPTION == "2" ]; then
        spec=$spec32
        CHOICE="32"
    fi
    echo "*** You have selected ${CHOICE}-bit architecture."
fi

echo "*** Creating Farseer-NMR environment..."
specfile="$(pwd)/Documentation/${spec}"

if conda create --name farseernmr --file $specfile; then
    echo "*** Miniconda environment successfully installed"
else
    echo "*** ERROR: Cannot configure Miniconda environment" >&2
    echo "*** Please confirm you have at least 4GB of free disk space"
    echo "*** Exiting..."
    exit 1
fi
echo "*** Done..."

echo
echo "*** Configuring run_farseer.sh file..."
tee run_farseer.sh <<< \
"#!/usr/bin/env bash

export FARSEER_ROOT=\"$(pwd)\"
export PYTHONPATH=\$PYTHONPATH:\${FARSEER_ROOT}

source activate farseernmr

python \$FARSEER_ROOT/gui/main.py \$*
"
chmod u+x run_farseer.sh
echo "*** Done..."
echo
echo \
"   *****
    
    Farseer-NMR as been correctly configured and
    
    TO LAUNCH FARSEER-NMR:
    
    ./run_farseer.sh
    
    or
    
    double click on the run_farseer.sh file
    
    :-)
"
