#/bin/bash

./postgres/bin/restart.sh
./gillard/bin/build.sh && ./gillard/bin/restart.sh
