FROM nginx:1.19-alpine

COPY nginx.conf /etc/nginx/nginx.conf

# Create backup directory with sensitive files (for challenge #22)
RUN mkdir -p /var/www/backup && \
    echo "FLAG{d1r3ct0ry_l1st1ng_3xp0s3s_f1l35}" > /var/www/backup/flag.txt && \
    echo "db_host=mysql\ndb_user=root\ndb_pass=root\njwt_secret=secret123" > /var/www/backup/config.bak && \
    echo "[users]\nadmin:Adm1n@InnovateTech2024\ndevops:D3v0ps@2024" > /var/www/backup/credentials.txt

EXPOSE 80 8080
