# -*- coding: utf-8 -*-

import sys

def y_or_n(prompt, default=None):
    if default == 'y':
        yorn_str = "Y/n"
    elif default == 'n':
        yorn_str = "y/N"
    else:
        yorn_str = "y/n"

    while True:
        sys.stdout.write("%s [%s]: " % (prompt, yorn_str))
        line = sys.stdin.readline().strip()
        if (not line) and default:
            return default
        elif line and line[0].lower() == 'n':
            return 'n'
        elif line and line[0].lower() == 'y':
            return 'y'
