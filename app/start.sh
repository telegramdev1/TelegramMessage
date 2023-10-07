#!/bin/bash
nohup python3 app.py > /dev/null &
nohup python3 tgMessage_receiver.py > /dev/null &
