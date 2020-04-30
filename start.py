#!/usr/bin/env python3

import argparse
import contextlib
import os, re, subprocess, sys

def log(s):
    sys.stderr.write("start to run: ")
    sys.stderr.write(s)
    sys.stderr.write("\n")
    sys.stderr.flush()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true")
    group.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("-ey", "--entity", choices=["AU", "SG"], help="choice entity")
    parser.add_argument("-ev", "--env", choices=["sit", "uat"], help="choice env")
    args = parser.parse_args()

    if args.quiet:
        sys.exit()
    elif args.entity and args.env:
        log("entity is {}， env is {}".format(args.entity, args.env))
    else:
        log("\nTry './start -h' to get more. \n")