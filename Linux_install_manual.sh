#!/bin/bash

tee run_farseer.sh <<< \
"#!/usr/bin/env bash

export FARSEER_ROOT=\"$(pwd)\"
export PYTHONPATH=\$PYTHONPATH:\${FARSEER_ROOT}

python \$FARSEER_ROOT/gui/main.py \$*
"

chmod u+x run_farseer.sh

echo \
"
    run_farseer.sh has been created.
    you may wish to complete this file with
    the necessary EXPORTS according to your Python setup.
    
    TO RUN FARSEER-NMR:
    
    ./run_farseer.sh
    
    :-)
"
