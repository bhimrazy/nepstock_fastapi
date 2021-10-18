#!/bin/bash

# Author : Bhimraj Yadav
# Copyright (c) bhimraj.com.np
# Script follows here:

# Local .env
if [ -f .env ]; then
    # Load Environment Variables
    export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
fi

echo "***** Running setup of Deta CLI *****"

curl -fsSL https://get.deta.dev/cli.sh | sh

echo "***** Deta was installed successfully to /home/gitpod/.deta/bin/deta *****"

source ~/.bashrc

echo "***** Exporting Token *****"

export DETA_ACCESS_TOKEN=$ACCESS_TOKEN

echo "***** Completed *****"

export PYTHONPATH="$PYTHONPATH:$HOME/.python"
