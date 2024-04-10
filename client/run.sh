#!/bin/sh

sed -i "s@const API_BASE_URL = process.env.API_BASE_URL?.trim();@const API_BASE_URL = \"${API_BASE_URL}\";@g" nuxt.config.ts

npm run build
node .output/server/index.mjs
