#!/bin/bash

sudo yum upgrade -y
sudo yum install git -y

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
exec "$SHELL"

pyenv install 3.6.6

pip install -u pip
pip install -u numpy pandas requests synapseclient