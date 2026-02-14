#!/bin/bash
grep -Eq 'smtpd_tls_security_level\s*=\s*(may|encrypt)' /etc/postfix/main.cf && echo "STARTTLS configured" || echo "STARTTLS not configured"
