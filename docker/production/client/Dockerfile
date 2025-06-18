FROM docker.io/node:20.11-alpine3.18 AS base


FROM base AS deps

RUN apk add --no-cache libc6-compat

ARG APP_HOME=/app
WORKDIR ${APP_HOME}

COPY client/package.json client/yarn.lock* client/package-lock.json* client/pnpm-lock.yaml* ./

RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i; \
  else echo "Lockfile not found." && exit 1; \
  fi


FROM base AS builder
ARG APP_HOME=/app
WORKDIR ${APP_HOME}


COPY --from=deps /app/node_modules ./node_modules

COPY client/. ${APP_HOME}

COPY client/.env.production .env.production

RUN npm run build


FROM base AS runner

ARG APP_HOME=/app
WORKDIR ${APP_HOME}

ENV NODE_ENV=production

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

ENV PORT 3000

CMD HOSTNAME=client node server.js
