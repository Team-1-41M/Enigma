FROM node:latest

RUN mkdir -p /usr/src/enigma/client/
WORKDIR /usr/src/enigma/client/

COPY . .
RUN npm install

CMD ["npm", "run", "dev"]