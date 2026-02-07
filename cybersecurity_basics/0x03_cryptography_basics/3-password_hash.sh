#!/usr/bin/env bash
R=$(openssl rand -hex 8); echo "$1$R" | tr -d '\n' | openssl dgst -sha512 > 3_hash.txt
