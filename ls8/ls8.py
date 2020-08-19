#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

read = sys.argv[1]
cpu.load(read)
cpu.run()