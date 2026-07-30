FROM postgres:18-alpine

LABEL maintainer="KOTS"

# Copy any custom init scripts (run once on first boot)
COPY init/ /docker-entrypoint-initdb.d/

COPY entrypoint.sh /

RUN chmod +x /entrypoint.sh

# Optional: custom postgresql.conf tweaks
COPY postgresql.conf /etc/postgresql/postgresql.conf

ENTRYPOINT [ "/entrypoint.sh" ]

CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]