#!/bin/bash

export CONDA_ROOT="$(pwd)/miniconda3/envs/farseernmr"
export FARSEER_ROOT="$(pwd)"
export PYTHONPATH=${CONDA_ROOT}:${FARSEER_ROOT}

$CONDA_ROOT/bin/python $FARSEER_ROOT/main.py \$\*
