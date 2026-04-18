#!/usr/bin/bash
grep "new user" auth.log | awk -F"name=" '{print $2}' | awk -F"," '{print $1}' | sort  | paste -sd ","
