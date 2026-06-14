FROM ubuntu/bind9:latest

COPY named.conf /etc/bind/named.conf
COPY zones/ /etc/bind/zones/

RUN chown -R bind:bind /etc/bind/zones

EXPOSE 53/udp
EXPOSE 53/tcp

CMD ["named", "-g", "-c", "/etc/bind/named.conf", "-u", "bind"]
