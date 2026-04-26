#!/bin/bash
nmap -p80,443 --script http-vuln-cve2017-5638 "$1" > comprehensive_scan_results.txt && nmap -p443 --script ssl-enum-ciphers "$1" >> comprehensive_scan_results.txt && nmap -p21 --script ftp-anon "$1" >> comprehensive_scan_results.txt
