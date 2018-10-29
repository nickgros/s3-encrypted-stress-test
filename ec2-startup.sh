#!/bin/bash

sudo yum upgrade -y
sudo yum install bzip2-devel gcc git libssl-dev readline-devel zlib-devel -y

sudo yum install gcc git zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel libffi-devel -y

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
exec "$SHELL"

curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

pyenv install 3.6.7
pyenv global 3.6.7

pip install --upgrade pip
pip install --upgrade numpy pandas requests synapseclient