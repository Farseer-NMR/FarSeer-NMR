#!/usr/bin/env bash

export CONDA_ROOT="$(pwd)/miniconda3"

miniconda32="Miniconda3-latest-Linux-x86.sh"
miniconda64="Miniconda3-latest-Linux-x86_64.sh"
spec32="spec-file_32bit.txt"
spec64="spec-file_64bit.txt"

# Miniconda doesn't work for directory structures with spaces
if [[ $(pwd) == *" "* ]]
then
    echo "ERROR: Cannot install into a directory with a space in its path" >&2
    echo "Exiting..."
    echo
    exit 1
fi

echo "*** Reading computer architecture..."

# https://stackoverflow.com/questions/7066625/how-to-find-the-linux-processor-chip-architecture
architecture=$(lscpu | grep Architecture)

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
    minicondaversion=$miniconda64
    spec=$spec64
    echo "*** Found 64-bit architecture!"
    echo

elif [ $arch == $bit32 ]; then
    minicondaversion=$miniconda32
    spec=$spec32
    echo "*** Found 32-bit architecture!"
    echo
else
    OPTION="99"
    while [ $OPTION != "1" -a  $OPTION != "2" ]; do
        queryuser
    done
    
    if [ $OPTION == "1" ]; then
        minicondaversion=$miniconda64
        spec=$spec64
        CHOICE="64"
    elif [ $OPTION == "2" ]; then
        minicondaversion=$miniconda32
        spec=$spec32
        CHOICE="32"
    fi
    echo "*** You have selected ${CHOICE}-bit architecture."
fi

echo
echo "*** Downloading Miniconda from https://repo.continuum.io/miniconda/${minicondaversion}"
echo
wget "https://repo.continuum.io/miniconda/${minicondaversion}"

echo
echo "*** Starting Miniconda installation..."
echo
chmod u+x $minicondaversion
bash $minicondaversion -b -f -p $CONDA_ROOT

echo
echo "*** Creating Farseer-NMR environment..."
specfile="$(pwd)/Documentation/${spec}"
$CONDA_ROOT/bin/conda create --name farseernmr --file $specfile

echo "*** Configuring run_farseer.sh file..."

tee run_farseer.sh <<< \
"#!/usr/bin/env bash

export CONDA_ROOT=\"$(pwd)/miniconda3/envs/farseernmr\"
export FARSEER_ROOT=\"$(pwd)\"
export PYTHONPATH=\${CONDA_ROOT}:\${FARSEER_ROOT}

\$CONDA_ROOT/bin/python \$FARSEER_ROOT/gui/main.py \$*
"
chmod u+x run_farseer.sh
echo "*** Done..."
echo "*** Cleaning..."
# cleaning
rm $minicondaversion

echo \
"   *****
    
    Farseer-NMR as been correctly configured
    
    TO LAUNCH FARSEER-NMR:
    
    ./run_farseer.sh
    
    :-)
"
