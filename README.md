# 🔐 InnovateTech Security Lab
## Complete Cybersecurity Workshop — 50 Challenges

A beginner-to-advanced cybersecurity lab simulating a fictional company's vulnerable infrastructure.
Everything runs locally with **`docker compose up`** — no internet needed.

---

## 🚀 Quick Start

```bash
# 1. Start the lab (takes 3-5 minutes first time)
cd E-HACKING-LAB
docker compose up --build

# 2. Open the CTF Platform
http://localhost:3000

# 3. Target site
http://localhost

# 4. All services are on localhost
```

---

## 🗺️ Service Map

| Service | Port | Purpose | Credentials |
|---|---|---|---|
| **CTF Platform** | 3000 | Challenge dashboard | None needed |
| **Vuln Web App** | 80 | Main target site | See challenges |
| **Vuln API** | 4000 | JWT/GraphQL API | user:password123 |
| **MySQL** | 3306 | Database (exposed) | root:root |
| **Redis** | 6379 | Cache (no auth) | None |
| **MongoDB** | 27017 | NoSQL DB (no auth) | None |
| **FTP** | 21 | Anonymous FTP | anonymous:anything |
| **SSH Target** | 2222 | Linux priv-esc box | user:password123 |
| **DNS** | 5353 | Zone transfer vuln | None |
| **Elasticsearch** | 9200 | No-auth index | None |
| **Banner Service** | 8888 | Hidden service | nc connect |

---

## 📚 Workshop Flow (4 Hours)

### Phase 1 — Network Recon (45 min) — Challenges 1-10
> "Before attacking, we need to SEE."

```
Tools needed: nmap, netcat, redis-cli, mongosh, mysql, dig
```
1. **Scan all ports** → find hidden service on 8888
2. **FTP anonymous login** → download files
3. **Banner grabbing** → SSH reveals version + flag
4. **DNS zone transfer** → dump entire DNS zone
5. **Subdomain enumeration** → find admin subdomain
6. **Redis** → connect without auth, dump keys
7. **MongoDB** → connect without auth, dump collections
8. **MySQL** → direct connection with root:root
9. **HTTP headers** → X-Secret-Flag header
10. **Elasticsearch** → no-auth search index

**Key lesson**: Every open service is a potential entry point. Always map first!

---

### Phase 2 — Server & Linux (45 min) — Challenges 11-20

```
Tools needed: ssh, hydra, sudo, find, crontab
```

11. **SSH default creds** → user:password123
12. **SSH brute force** → admin:iloveyou (via hydra)
13. **SUID exploitation** → find has SUID set
14. **Sudo misconfiguration** → vim NOPASSWD → root
15. **Cron job abuse** → world-writable script run by root
16. **Writable /etc/passwd** → add root user
17. **.bash_history** → credentials in command history
18. **Env variables** → secrets in environment
19. **PATH hijacking** → fake binary in PATH
20. **Exposed SSH key** → in /backup/ web directory

**Key lesson**: Post-exploitation is about finding weak configurations, not just exploits.

---

### Phase 3 — Web Security Basics (60 min) — Challenges 21-35

```
Tools: browser, curl, Burp Suite
Target: http://localhost
```

21. **robots.txt** → reveals hidden paths
22. **Directory listing** → /backup/ exposed
23. **Default creds** → admin/admin123 on /admin
24. **SQLi login bypass** → `admin'--`
25. **SQLi UNION** → extract from hidden table
26. **Blind SQLi** → boolean-based extraction
27. **Reflected XSS** → `<script>alert(document.cookie)</script>` in search
28. **Stored XSS** → persist in comments
29. **CSRF** → change email without consent
30. **Path traversal** → `/download?file=../../../../etc/flag.txt`
31. **LFI** → `/page?template=../../secret/flag`
32. **Command injection** → `8.8.8.8; cat /flag.txt` in ping
33. **IDOR** → `/profile/999` → admin data
34. **Open redirect** → `/redirect?url=https://evil.com`
35. **HTTP verb tampering** → PUT to bypass GET restriction

**Key lesson**: Input is NEVER trusted. Every parameter is a potential vulnerability.

---

### Phase 4 — Advanced Web (45 min) — Challenges 36-45

```
Tools: jwt.io, hashcat, python3, curl
Target: http://localhost:4000 (API)
```

36. **JWT none algorithm** → forge admin token
37. **JWT weak secret** → crack "secret123" with hashcat
38. **API key in JS** → check /static/js/config.js
39. **SSRF** → `/api/fetch?url=http://internal-flag:9999/flag`
40. **XXE** → read files via XML external entity
41. **File upload RCE** → upload PHP webshell
42. **GraphQL introspection** → find hidden queries
43. **Insecure deserialization** → pickle RCE
44. **Clickjacking** → /tools/clickjack demo
45. **HTML comments** → secrets in page source

---

### Phase 5 — Real World (45 min) — Challenges 46-50

46. **Missing security headers** → audit with curl -I
47. **Log4Shell concept** → inject JNDI in User-Agent
48. **Exposed .env** → `curl http://localhost/.env`
49. **Rate limiting test** → flood login endpoint
50. **Full chain** → combine everything to get FINAL_FLAG

---

## 🎓 Instructor Notes

### Hint System
- Hint 1 unlocks after **1 failed attempt**
- Hint 2 unlocks after **3 failed attempts**
- Hint 3 unlocks after **5 failed attempts**
- Solution unlocks after **6 failed attempts** (with confirmation dialog)

### Classroom Tips
1. Start with Challenge #1 as a live demo (nmap scan)
2. Group students in pairs for first few challenges
3. Pause at each phase to explain real-world context
4. Use the timer at top of platform (4 hour countdown)
5. Encourage students to explore beyond the challenge hints

### Quick Commands Cheatsheet

```bash
# Port scan
nmap -sV -p- localhost

# FTP anonymous
ftp localhost 21   # user: anonymous, pass: anything

# Redis
redis-cli -h localhost KEYS '*'
redis-cli -h localhost GET FLAG

# MongoDB
mongosh localhost:27017
use flagsdb; db.flags.find()

# MySQL
mysql -h 127.0.0.1 -u root -proot innovatetech
SELECT * FROM flags;

# DNS zone transfer
dig AXFR innovatetech.local @127.0.0.1 -p 5353

# SSH
ssh -p 2222 user@localhost   # password: password123

# Hidden service
nc localhost 8888

# Elasticsearch
curl http://localhost:9200/internal-secrets/_search?pretty

# JWT decode
echo 'PAYLOAD_PART' | base64 -d

# SQLi test
curl "http://localhost/search?q=test' UNION SELECT 1,flag,3 FROM secret_data--"

# Command injection
curl http://localhost/tools/ping -d "ip=8.8.8.8; cat /flag.txt" -X POST

# Path traversal
curl "http://localhost/download?file=../../../../etc/flag.txt"

# SSRF
curl "http://localhost/api/fetch?url=http://internal-flag:9999/flag"

# API key
curl -H "X-API-Key: sk-prod-7f3k9x2mAbCdEf123456" http://localhost:4000/api/admin/secret

# GraphQL introspection
curl -X POST http://localhost:4000/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query":"{__schema{queryType{fields{name}}}}"}'
```

---

## 🛡️ Security Concepts Covered

| Concept | Real-World Impact | Challenge # |
|---|---|---|
| Open ports / recon | Every exposed service is attacked | 1, 9, 10 |
| Default credentials | Mirai botnet — 600K devices | 11, 23 |
| Weak passwords | 80% of breaches involve weak passwords | 12 |
| SQL Injection | OWASP #3, affects 30% of web apps | 24, 25, 26 |
| XSS | Twitter worm 2010, 500K users in 2h | 27, 28 |
| CSRF | Facebook, Gmail, PayPal all affected | 29 |
| Path Traversal | Read any file on server | 30, 31 |
| Command Injection | Full server takeover | 32 |
| IDOR | Instagram bug exposed 500M phone numbers | 33 |
| JWT attacks | Auth bypass, identity spoofing | 36, 37 |
| SSRF | Capital One breach, $80M fine | 39 |
| XXE | Billion-laughs DoS, data exfil | 40 |
| File Upload RCE | Complete server compromise | 41 |
| Log4Shell | CVE-2021-44228, CVSS 10.0 | 47 |
| DNS zone transfer | Reveals entire network map | 4, 5 |
| Redis/MongoDB no-auth | Millions of records exposed in 2017 | 6, 7 |

---

## 🔧 Troubleshooting

```bash
# Check all containers are running
docker compose ps

# View logs
docker compose logs webapp
docker compose logs platform

# Restart a service
docker compose restart webapp

# Reset all data (fresh start)
docker compose down -v && docker compose up --build

# If MySQL takes too long
docker compose logs mysql  # wait for "ready for connections"
```

---

## ⚠️ Important

This lab is **intentionally vulnerable**. Run it only:
- In an isolated local environment
- On a private network (not public WiFi)
- For educational purposes only

**Never** expose these containers to the internet.

---

*Built for the Cyberecurity Workshop — Teaching real-world security concepts through hands-on labs.*
