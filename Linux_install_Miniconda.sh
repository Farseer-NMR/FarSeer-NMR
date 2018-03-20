#!/usr/bin/env bash

export CONDA_ROOT="$(pwd)/miniconda3"

# Miniconda doesn't work for directory structures with spaces
if [[ $(pwd) == *" "* ]]
then
    echo "ERROR: Cannot install into a directory with a space in its path" >&2
    echo "Exiting..."
    echo
    exit 1
fi

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
    minicondaversion="Miniconda3-latest-Linux-x86_64.sh"
    spec="spec-file_64bit.txt"
    echo "Found 64-bit architecture..."
fi

if [ "$arch" == "$bit32" ]
then
    minicondaversion="Miniconda3-latest-Linux-x86.sh"
    spec="spec-file_32bit.txt"
    echo "Found 32-bit architecture..."
fi

wget "https://repo.continuum.io/miniconda/${minicondaversion}"
chmod a+rwx $minicondaversion
bash $minicondaversion -b -f -p $CONDA_ROOT

chmod u+rwx run_farseer.sh
specfile="$(pwd)/Documentation/${spec}"

$CONDA_ROOT/bin/conda create --name farseernmr --file $specfile

tee run_farseer.sh <<< \
'#!/usr/bin/env bash

export CONDA_ROOT="$(pwd)/miniconda3/envs/farseernmr"
export FARSEER_ROOT="$(pwd)"
export PYTHONPATH=${CONDA_ROOT}:${FARSEER_ROOT}

$CONDA_ROOT/bin/python $FARSEER_ROOT/gui/main.py $*
'

chmod u+x run_farseer.sh

echo \
"   *****
    
    Farseer-NMR as been correctly configured and
    
    TO LAUNCH FARSEER-NMR:
    
    ./run_farseer.sh
    
    :-)
"

# cleaning
rm $minicondaversion
