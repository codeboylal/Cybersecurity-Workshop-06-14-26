FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    openssh-server \
    sudo \
    vim \
    python3 \
    curl \
    wget \
    net-tools \
    cron \
    findutils \
    && rm -rf /var/lib/apt/lists/*

# Create vulnerable user accounts
RUN useradd -m -s /bin/bash user && echo "user:password123" | chpasswd
RUN useradd -m -s /bin/bash admin && echo "admin:iloveyou" | chpasswd
RUN useradd -m -s /bin/bash devops && echo "devops:D3v0ps@2024" | chpasswd

# Setup SSH
RUN mkdir -p /var/run/sshd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Set root password
RUN echo "root:toor" | chpasswd

# Create flag files
RUN echo "FLAG{ssh_d3f4ult_cr3d5_4r3_d34dly}" > /home/user/flag.txt && \
    chown user:user /home/user/flag.txt

RUN echo "FLAG{w34k_p455w0rd5_4r3_3z_br34k}" > /home/admin/flag.txt && \
    chown admin:admin /home/admin/flag.txt

RUN mkdir -p /root && \
    echo "FLAG{su1d_b1n4r13s_4r3_pr1v_3sc}" > /root/flag_suid.txt && \
    echo "FLAG{sud0_n0p4sswd_1s_r00t}" > /root/flag_sudo.txt && \
    echo "FLAG{cr0n_j0b_wr1t3_4nd_0wn}" > /root/flag_cron.txt && \
    echo "FLAG{wr1t4bl3_p455wd_1s_g4m3_0v3r}" > /root/flag_passwd.txt && \
    echo "FLAG{p4th_h1j4ck_g4v3_m3_r00t}" > /root/flag_path.txt && \
    echo "FLAG{priv4t3_k3y_l3ft_1n_publ1c}" > /root/flag_sshkey.txt && \
    echo "FLAG{full_ch41n_3xpl01t_m4st3r}" > /root/FINAL_FLAG.txt

# Challenge #13: SUID binary (find gets SUID)
RUN chmod u+s /usr/bin/find

# Challenge #14: Sudo misconfiguration
RUN echo "user ALL=(root) NOPASSWD: /usr/bin/vim" >> /etc/sudoers && \
    echo "user ALL=(root) NOPASSWD: /usr/bin/python3" >> /etc/sudoers

# Challenge #15: Cron job with world-writable script
RUN echo '#!/bin/bash\necho "Backup running at $(date)" >> /var/log/backup.log' > /opt/cleanup.sh && \
    chmod 777 /opt/cleanup.sh && \
    echo "* * * * * root /opt/cleanup.sh" >> /etc/crontab

# Challenge #16: World-writable /etc/passwd
RUN chmod 666 /etc/passwd

# Challenge #17: bash_history with credentials
RUN echo 'mysql -u admin -p'"'"'SecretDB@2024'"'"' -h db.internal' >> /home/user/.bash_history && \
    echo 'curl -u admin:P@ssw0rd123 http://internal-api/v1/users' >> /home/user/.bash_history && \
    echo 'cat /root/flag_hist.txt' >> /home/user/.bash_history && \
    echo 'ssh admin@10.0.1.5 -i ~/.ssh/id_rsa_backup' >> /home/user/.bash_history && \
    echo 'FLAG{h1st0ry_l34k5_s3cr3t5}' >> /home/user/.bash_history && \
    chown user:user /home/user/.bash_history

# Challenge #18: Environment variable with secret
RUN echo 'export SECRET_FLAG="FLAG{3nv_v4r5_4r3_n0t_s3cr3t}"' >> /home/user/.bashrc && \
    echo 'export API_KEY="sk-internal-9f3kAbCd"' >> /home/user/.bashrc && \
    echo 'export DB_PASSWORD="root"' >> /home/user/.bashrc

# Custom SSH banner showing flag (challenge #3)
RUN echo "##################################################" > /etc/ssh/banner.txt && \
    echo "#  InnovateTech SSH Server v7.6p1 Ubuntu 22.04  #" >> /etc/ssh/banner.txt && \
    echo "#                                                #" >> /etc/ssh/banner.txt && \
    echo "#  FLAG{b4nn3r5_r3v34l_v3rs10n5}                #" >> /etc/ssh/banner.txt && \
    echo "#                                                #" >> /etc/ssh/banner.txt && \
    echo "#  WARNING: Unauthorized access is prohibited    #" >> /etc/ssh/banner.txt && \
    echo "##################################################" >> /etc/ssh/banner.txt && \
    echo "Banner /etc/ssh/banner.txt" >> /etc/ssh/sshd_config

# Challenge #19: PATH hijacking setup
RUN echo '#!/bin/bash\nservice backup start' > /opt/backup_script.sh && \
    chmod +x /opt/backup_script.sh && \
    echo "user ALL=(root) NOPASSWD: /opt/backup_script.sh" >> /etc/sudoers

# Challenge #20: Exposed SSH key in /tmp (accessible via web /backup/id_rsa)
RUN ssh-keygen -t rsa -b 2048 -f /root/.ssh/lab_key -N "" && \
    cp /root/.ssh/lab_key.pub /root/.ssh/authorized_keys && \
    cp /root/.ssh/lab_key /tmp/backup_key

EXPOSE 22

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
