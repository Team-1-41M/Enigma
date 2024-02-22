// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  srcDir: "src/",
  ssr: false,
  css: ['~/assets/css/main.css'],
  modules: [
    '@pinia/nuxt'
  ],
  runtimeConfig: {
    public: {
      baseUrl: process.env.API_BASE_URL
    }
  }
})
