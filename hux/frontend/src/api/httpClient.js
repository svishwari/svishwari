/**
 * HTTP client configured for the API client for managing http requests.
 */

import axios from "axios"
import config from "@/config"
import Vue from "vue"

const httpClient = axios.create({
  baseURL: `${config.apiUrl}${config.apiBasePath}`,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
    "Cache-Control": "no-cache",
  },
})

if (process.env.NODE_ENV !== "test") {
  httpClient.interceptors.request.use(async (config) => {
    const accessToken = await Vue.prototype.$auth.getAccessToken()
    const idToken = await Vue.prototype.$auth.getIdToken()
    config.headers.Authorization = `Bearer ${accessToken}`
    config.headers.AuthorizationDen = `Bearer ${idToken}`
    return config
  })
}

export default httpClient
