/**
 * HTTP client configured for the API client for managing http requests.
 */

import axios from "axios"
import config from "@/config"
impo

const httpClient = axios.create({
  baseURL: `${config.apiUrl}${config.apiBasePath}`,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
})

httpClient.interceptors.request.use(async (config) => {
  const accessToken = localStorage.token
  config.headers.Authorization = `Bearer ${accessToken}`
  return config
})

export default httpClient
