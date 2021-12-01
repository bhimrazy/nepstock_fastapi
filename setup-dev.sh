#!/bin/bash

# Author : Bhimraj Yadav
# Copyright (c) bhimraj.com.np
# Script follows here:

# clear previous venv folder if exists
DIR="./venv"
if [ -d "$DIR" ]; then
  # Take action if $DIR exists. #
  echo "Removing ${DIR} ..."
  rm -rf venv
fi
echo "Upgrading pip...."
python -m pip install --upgrade pip

# create a virtual environment and activate it
echo "Creating a virtual environment."
python -m venv venv
source venv/bin/activate
echo "Virtual Environment activated."

export PIP_USER=false

# install required packages
echo "Installing requirements....."
pip install -r requirements.txt

# run app
uvicorn app.main:app --reload