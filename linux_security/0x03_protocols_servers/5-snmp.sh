#!/bin/bash
grep -vE '^#|^$' /etc/snmp/snmpd.conf | grep 'public'
