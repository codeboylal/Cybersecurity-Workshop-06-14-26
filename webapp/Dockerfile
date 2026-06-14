FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    default-mysql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create upload directory and flag files
RUN mkdir -p /app/uploads /app/backup /etc
RUN echo "FLAG{p4th_tr4v3rs4l_r34ds_4ny_f1l3}" > /etc/flag.txt
RUN echo "FLAG{lf1_1nclud3s_s3cr3t_f1l3s}" > /app/secret/flag.txt || (mkdir -p /app/secret && echo "FLAG{lf1_1nclud3s_s3cr3t_f1l3s}" > /app/secret/flag.txt)
RUN echo "FLAG{cmd_1nj3ct10n_0wns_th3_s3rv3r}" > /flag.txt
RUN echo "FLAG{xxe_r34d5_l0c4l_f1l35}" >> /etc/flag.txt
RUN echo "FLAG{f1l3_upl04d_rce_g4m3_0v3r}" > /app/flag_upload.txt
RUN echo "FLAG{d3s3r14l1z4t10n_rce_pwn3d}" > /app/flag_deser.txt

EXPOSE 5000

CMD ["python", "app.py"]
