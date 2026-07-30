
FROM node:24-alpine AS dev

ENV COREPACK_ENABLE_DOWNLOAD_PROMPT=0
#requirements.txt can be used for the packages, vite is installed with vue

# git init && git add -A && git commit -m "initial commit" it says to add this after pnpm dev
#RUN create vue@latest app --default --jsx --eslint --prettier --oxfmt
#    && cd test2 && pnpm install && pnpm format && pnpm dev

# look how to change the lookup directory of srcs for vue and vite

RUN corepack enable pnpm


# Cache dependencies
#COPY package.json pnpm-lock.yaml* ./
#RUN pnpm install

# Copy your source code (will be overridden by compose bind-mount during dev)
#COPY index.html vite.config.js .

EXPOSE 5173

WORKDIR /app

# The actual execution command when the container boots
CMD ["sh", "-c", "pnpm clean --lockfile && pnpm install && pnpm format && pnpm dev --host"]


FROM node:24-alpine AS prod

ENV COREPACK_ENABLE_DOWNLOAD_PROMPT=0
#requirements.txt can be used for the packages, vite is installed with vue

# git init && git add -A && git commit -m "initial commit" it says to add this after pnpm dev
#RUN create vue@latest app --default --jsx --eslint --prettier --oxfmt
#    && cd test2 && pnpm install && pnpm format && pnpm dev

# look how to change the lookup directory of srcs for vue and vite

RUN corepack enable pnpm


# Cache dependencies
#COPY package.json pnpm-lock.yaml* ./
#RUN pnpm install

# Copy your source code (will be overridden by compose bind-mount during dev)
#COPY index.html vite.config.js .
WORKDIR /app
COPY ./app/ .
CMD ["pnpm", "run", "build"]
