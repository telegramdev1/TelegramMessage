#!/bin/bash
nohup python3 app.py > /dev/null &
nohup python3 tgMessage_reciver.py > /dev/null &