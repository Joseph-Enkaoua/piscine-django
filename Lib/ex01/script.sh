#!/bin/bash

pip3 --version
python3 -m venv local_lib
source local_lib/bin/activate
pip3 install --log pip_install.log -I git+https://github.com/jaraco/path.git
pip list

python3 my_program.py