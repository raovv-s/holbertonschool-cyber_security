#!/usr/bin/bash
grep "pam_unix" auth.log | awk -F'(' '{print $2}' | awk -F':' '{print $1}' | sort | uniq -c | sort -nr
