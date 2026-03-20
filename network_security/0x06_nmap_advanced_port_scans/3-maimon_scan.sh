#!/bin/bash
sudo nmap -sM -phttp,ftp,telnet,https,ssh $1 -vv
