
FROM node:24-alpine

WORKDIR /app
#requirements.txt can be used for the packages, vite is installed with vue
RUN corepack enable pnpm && pnpm install vue

# git init && git add -A && git commit -m "initial commit" it says to add this after pnpm dev
RUN mkdir vue_app && create vue@latest vue_app --default --jsx --eslint --prettier --oxfmt && cd test2 && pnpm install && pnpm format && pnpm dev

# look how to change the lookup directory of srcs for vue and vite