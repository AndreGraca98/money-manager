ARG NODE_VERSION=20.12.2

FROM node:${NODE_VERSION}-alpine as builder
WORKDIR /app
RUN yarn global add @quasar/cli
COPY package.json yarn.lock .
RUN yarn install
COPY . .
RUN quasar build

FROM nginx:alpine as runner
WORKDIR /usr/share/nginx/html
COPY --from=builder /app/dist/spa .
COPY default.conf /etc/nginx/conf.d/default.conf
