#!/bin/bash
sudo nmap -sM -p21,22,20,80,443 $1 -vv
