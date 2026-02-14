#!/bin/bash
nmap --script ssl-enum-ciphers -p 443 "$1" | grep -Ei 'weak|3des|rc4|des|md5|export'
