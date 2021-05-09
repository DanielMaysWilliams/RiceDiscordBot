#!/bin/bash
source ~/.profile
tmux kill-session -t discord
tmux new-session -d -s discord '/home/pi/software/ChickenKitchenBot/pull_and_start.sh' 
