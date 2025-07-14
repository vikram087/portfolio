#!/bin/bash

tmux kill-server
cd portfolio
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
pip install -r requirements.txt
tmux new-session -d -s flask-server -c /root/portfolio \; send-keys "source python3-virtualenv/bin/activate" Enter \; send-keys "flask run --host=0.0.0.0" Enter

