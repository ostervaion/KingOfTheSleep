# Step 1: Build Caddy with the Coraza WAF plugin
FROM caddy:2-builder AS builder

RUN xcaddy build \
    --with github.com/corazawaf/coraza-caddy/v2 \
    --with github.com/DeRuina/timberjack \
    --with github.com/mholt/caddy-ratelimit
# Step 2: Assemble the final production image
FROM caddy:2-alpine AS dev

COPY --from=builder /usr/bin/caddy /usr/bin/caddy
COPY Caddyfile_dev /etc/caddy/Caddyfile

FROM caddy:2-alpine AS prod

COPY --from=builder /usr/bin/caddy /usr/bin/caddy
COPY Caddyfile /etc/caddy/Caddyfile