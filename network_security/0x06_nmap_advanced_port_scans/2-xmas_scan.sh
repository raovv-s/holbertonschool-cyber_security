#!/bin/bash
#!/bin/bash

nmap -sX -p 440-450 --open --packet-trace --reason $1
