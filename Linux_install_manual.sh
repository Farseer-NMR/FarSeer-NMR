#!/bin/bash

echo
echo "*** Configuring run_farseer_gui.sh file..."
echo
tee run_farseer.sh <<< \
"#!/usr/bin/env bash

export FARSEER_ROOT=\"$(pwd)\"
export PYTHONPATH=\$PYTHONPATH:\${FARSEER_ROOT}

python \$FARSEER_ROOT/gui/main.py \$*
"
chmod u+x run_farseer.sh

echo
echo "*** Configuring exec_farseer_commandline.sh file..."
echo
tee exec_farseer_commandline.sh <<< \
"#!/usr/bin/env bash

export FARSEER_ROOT=\"$(pwd)\"
export PYTHONPATH=\$PYTHONPATH:\${FARSEER_ROOT}

python \$FARSEER_ROOT/core/farseermain.py \$*
"
chmod u+x exec_farseer_commandline.sh

echo "*** Done..."
echo
echo \
"
    Farseer-NMR run files have been correctly configured.

    You may wish to complete this file with
    the necessary EXPORTS according to your Python setup.
    
    TO RUN FARSEER-NMR GUI:
    
    ./run_farseer.sh
    
    or double click on the file :-)
"