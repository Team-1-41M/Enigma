FROM node:latest

RUN mkdir -p /usr/src/enigma/client/

WORKDIR /usr/src/enigma/client/

COPY . .

RUN npm install
RUN npx nuxi build

ENTRYPOINT [ "bash", "-c", "rm -rf /tmp/nitro/worker-* && node .output/server/index.mjs" ]