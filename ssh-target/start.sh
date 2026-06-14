#!/bin/bash
# Start cron
service cron start 2>/dev/null || true
# Start SSH
/usr/sbin/sshd -D
