#!/bin/bash
sudo apt-get update -y
sudo apt-get install -y python3-venv
python3 -m venv venv
source ./venv/bin/activate

echo Enter Venv for install python packages
pip install -r requirements.txt
