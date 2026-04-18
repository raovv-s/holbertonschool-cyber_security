#!/usr/bin/bash
grep "Accepted password for root" auth.log | awk -F" " '{print $11}' | sort | uniq -c | wc -l
