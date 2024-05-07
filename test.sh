#! bash

mkdir -p run
mkdir -p plans

python3 run.py -s instances/scenarios/random24-1.scen -m instances/maps/random24.map -a 20 -t 360000 -p picat-soc-split-all
