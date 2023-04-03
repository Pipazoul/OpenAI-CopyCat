FROM node:lts-slim as prod

WORKDIR /app

COPY src/ /app/src
COPY static/ /app/static
COPY .eslintignore /app/.eslintignore
COPY .eslintrc.cjs /app/.eslintrc.cjs
COPY package-lock.json /app/package-lock.json
COPY package.json /app/package.json
COPY postcss.config.cjs /app/postcss.config.cjs
COPY svelte.config.js /app/svelte.config.js
COPY tailwind.config.cjs /app/tailwind.config.cjs
COPY tsconfig.json /app/tsconfig.json
COPY vite.config.ts /app/vite.config.ts

RUN npm install

EXPOSE 5173

ENTRYPOINT [ "npm", "run", "dev"]