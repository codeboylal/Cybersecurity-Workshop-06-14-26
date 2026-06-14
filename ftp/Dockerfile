FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y vsftpd && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /srv/ftp/pub /var/run/vsftpd/empty

COPY vsftpd.conf /etc/vsftpd.conf

RUN echo "FLAG{4n0n_ftp_s3rv3r_l34k5_d4t4}" > /srv/ftp/pub/flag.txt
RUN printf "Welcome to InnovateTech FTP Server\nAnonymous access enabled.\nSee /pub/ for files.\n" > /srv/ftp/welcome.txt
RUN printf "db_host: mysql\ndb_user: root\ndb_pass: root\nredis: redis:6379\njwt_secret: secret123\napi_key: sk-prod-7f3k9x2mAbCdEf123456\n" > /srv/ftp/pub/credentials.txt
RUN printf "InnovateTech Internal Report\nSecurity Status: CRITICAL\nLast Audit: Never\nOpen Issues: 47\n" > /srv/ftp/pub/INTERNAL_REPORT.txt

EXPOSE 20 21 21100-21110

CMD ["/usr/sbin/vsftpd", "/etc/vsftpd.conf"]
