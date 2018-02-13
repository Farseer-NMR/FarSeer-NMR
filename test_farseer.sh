export FARSEER_ROOT="$(pwd)"
export PYTHONPATH=$FARSEER_ROOT

nosetests -w $FARSEER_ROOT/core/testing
nosetests -w $FARSEER_ROOT/gui/tabs/testing
nosetests -w $FARSEER_ROOT/gui/popups/testing
