#!/bin/sh

# Create virtual environment if it doesn't exist
if [ ! -d "comediq" ]; then
    python3 -m venv comediq
fi

# Activate virtual environment
. comediq/bin/activate

# Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt