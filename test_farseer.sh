export FARSEER_ROOT="$(pwd)"
export PYTHONPATH=$FARSEER_ROOT

nosetests -v -w $FARSEER_ROOT/core/testing
nosetests -v -w $FARSEER_ROOT/gui/tabs/testing
nosetests -v -w $FARSEER_ROOT/gui/popups/testing
