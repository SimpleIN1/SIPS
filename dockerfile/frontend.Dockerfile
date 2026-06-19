FROM node:24.12-alpine

RUN mkdir -p /usr/src/app/frontend/
WORKDIR /usr/src/app/frontend/

COPY ./frontend/package.json ./frontend/yarn.lock* ./

RUN npm install

COPY ./frontend .

RUN npm run build
CMD ls build
