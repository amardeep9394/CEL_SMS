#!/usr/bin/python

import os 

with open("/home/amardeep/Desktop/Server_version_0.3/data/msdState.json", 'r') as fh:
    first = next(fh)

    fh.seek(-2, os.SEEK_END)
    while fh.read(1) != b"\n":   # Until EOL is found...
        fh.seek(-2, os.SEEK_CUR) # ...jump back the read byte plus one more.
    last = fh.readline()

print last
