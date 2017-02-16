#!/usr/bin/env bash
python3 server.py > /dev/null &
cd test && python -m unittest discover
