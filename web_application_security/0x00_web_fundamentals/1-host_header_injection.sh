#!/bin/bash
curl -X POST -H "Host:$1" "$2" -d "$3"
# -d for data pasting -H Host -X http method
