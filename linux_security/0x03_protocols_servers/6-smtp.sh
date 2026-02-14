#!/bin/bash
grep -Eq '^[[:space:]]*smtpd_tls_security_level[[:space:]]*=[[:space:]]*(may|encrypt)' /etc/postfix/main.cf && echo "STARTTLS configured" || echo "STARTTLS not configured"
