#!/bin/bash

set -e
set -x

echo "installing python3 virtaul env"

rm -rf venv

python3 -m venv venv

venv/bin/python3 venv/bin/pip3 install -r requirements.txt --index-url=https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

rm -f start
ln -s start.sh start