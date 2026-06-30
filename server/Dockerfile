# Step 1: Build Caddy with the Coraza WAF plugin
FROM caddy:2-builder AS builder

RUN xcaddy build \
    --with github.com/corazawaf/coraza-caddy/v2 \
    # You can also add timberjack or your OTel extensions here if you still want them
    --with github.com/DeRuina/timberjack

# Step 2: Assemble the final production image
FROM caddy:2-alpine

COPY --from=builder /usr/bin/caddy /usr/bin/caddy
COPY Caddyfile /etc/caddy/Caddyfile
