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
  },
})

if (process.env.NODE_ENV !== "test") {
  httpClient.interceptors.request.use(async (config) => {
    const accessToken = await Vue.prototype.$auth.getAccessToken()
    config.headers.Authorization = `Bearer ${accessToken}`
    return config
  })
}

export default httpClient
