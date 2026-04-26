#!/bin/bash
nmap -p 80,443 --script http-vuln-cve2017-5638 "$1" -oN vuln_scan_results.txt
