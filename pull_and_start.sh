#!/bin/bash
cd /home/pi/software/ChickenKitchenBot
git pull
source discord/bin/activate
python bot.py
