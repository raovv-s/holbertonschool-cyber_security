#!/usr/bin/bash
grep "session opened for user root" auth.log | head -n 1 | awk -F"user " '{print $2}' | awk '{print $1}'
