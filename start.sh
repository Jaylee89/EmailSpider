#!/bin/bash

set -e

PYTHONWARNING="ignore:Unverified HTTPS request" $(dirname $0)/venv/bin/python3 $(dirname $0)/start.py "$@"