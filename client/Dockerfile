FROM node:latest

RUN mkdir -p /usr/src/enigma/client/

WORKDIR /usr/src/enigma/client/

COPY . .

RUN npm install

ENTRYPOINT [ "bash", "-c", "rm -rf /tmp/nitro/worker-* && chmod +x ./run.sh && ./run.sh" ]