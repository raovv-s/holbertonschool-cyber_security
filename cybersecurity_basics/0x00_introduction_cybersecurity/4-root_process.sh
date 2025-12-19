#!/bin/bash
ps aux -u "$1" u --no-headers | grep -v ' 0[[:space:]]\+0 '
