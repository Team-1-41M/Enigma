const API_DOMAIN = process.env.API_BASE_URL
    ?.replace(/^(http:\/\/)/, "")
    ?.replace(/^(https:\/\/)/, "")
    ?.replace(/\/*$/, "");

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    devtools: { enabled: true },
    srcDir: "src/",
    ssr: false,
    css: ['~/assets/css/main.css'],
    modules: [
        '@pinia/nuxt',
        '@nuxt-alt/proxy',
    ],
    proxy: {
        experimental: {
            listener: true,
        },
        proxies: {
            '/api': {
                target: `http://${API_DOMAIN}/api/v1`,
                rewrite: (path) => path.replace(/^\/api/, ''),
            },
            '/ws': {
                target: `ws://${API_DOMAIN}/api/v1`,
                rewrite: (path) => path.replace(/^\/ws/, ''),
                ws: true,
            },
        },
    },
    // https://nuxt.com/docs/guide/going-further/runtime-config
    runtimeConfig: {
        apiDomain: API_DOMAIN,
    }
})
