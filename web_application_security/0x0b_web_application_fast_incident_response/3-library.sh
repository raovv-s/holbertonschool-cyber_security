#!/usr/bin/env bash
cat logs.txt | awk -F '"' '{print $6}' | sort | uniq -c | sort -nr | head -n 1 | awk '{print $2}'
