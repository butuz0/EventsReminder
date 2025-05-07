FROM docker.io/node:20.11-alpine3.18 AS base

FROM base AS build-stage

RUN apk add --no-cache libc6-compat

COPY client/package.json client/yarn.lock* client/package-lock.json* client/pnpm-lock.yaml* ./

RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i; \
  else echo "Lockfile not found." && exit 1; \
  fi


FROM base AS run-stage

ARG APP_HOME=/app
WORKDIR ${APP_HOME}

COPY --from=build-stage /node_modules ./node_modules

COPY ./client ${APP_HOME}

CMD ["npm", "run", "dev"]