export FARSEER_ROOT="$(pwd)"

nosetests -w $FARSEER_ROOT/core/testing
nosetests -w $FARSEER_ROOT/gui/tabs/testing
nosetests -w $FARSEER_ROOT/gui/popups/testing
