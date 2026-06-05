FROM postgres:18-alpine

LABEL maintainer="your-team"

# Copy any custom init scripts (run once on first boot)
COPY init/ /docker-entrypoint-initdb.d/

# Optional: custom postgresql.conf tweaks
COPY postgresql.conf /etc/postgresql/postgresql.conf
