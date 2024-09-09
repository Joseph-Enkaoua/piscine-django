#!/bin/bash

pip3 --version
python3 -m venv local_lib
source local_lib/bin/activate
pip3 install --log pip_install.log -I git+https://github.com/jaraco/path.git
echo 'Printing installed modules in this environment:'
pip list

echo '=================== Executing the Python program ==================='
python3 my_program.py