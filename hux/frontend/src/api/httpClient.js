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
    config.headers.Authorization = `Bearer eyJraWQiOiIybHlKYjdrRTVYNEJLdm53WlIyYl9fSkFsMTh4WWVhQ2V6NGxPNUpYb1F3IiwiYWxnIjoiUlMyNTYifQ.eyJ2ZXIiOjEsImp0aSI6IkFULmE5c2d5Vk5IV2taUlJsTkJYeV9tVTVTRGgtYlFnNC02aUpwc2otLUR0ZE0iLCJpc3MiOiJodHRwczovL2RlbG9pdHRlZGlnaXRhbC1tcy5va3RhLmNvbSIsImF1ZCI6Imh0dHBzOi8vZGVsb2l0dGVkaWdpdGFsLW1zLm9rdGEuY29tIiwic3ViIjoic3Zpc2h3YXJpQGRlbG9pdHRlLmNvbSIsImlhdCI6MTY0MTk4MDUxOSwiZXhwIjoxNjQxOTg0MTE5LCJjaWQiOiIwb2FiMWkzbGRnWXlSdms1cjJwNyIsInVpZCI6IjAwdWJjdjBwMzFUR0JYOE9FMnA3Iiwic2NwIjpbIm9wZW5pZCIsImVtYWlsIiwicHJvZmlsZSJdfQ.uTN70uIFZgDJRyDEmuctZXZHaKqH4ms5n6sqwqOv-3XQWAoXsSKjh2ODe7lEps5tkRo9o_75LYaQqeDm5I9FyJz_PiLOoaQJiVdlJ4FxXzcqM39k2es5xALa2oG5u8h1bzSFxXvl_z0IjmOJAdQpk9sIYOaYAGZZo6Lp9YIgyIOBLhblc6a1fvgQu32Le-aSRl9wTKKn8Eo-BnZWrrX_9LkDTR8aR-Fa3Ci758go0CFnzYnM5rqu8mPfnAO3NJFYHwnFKr_8YKCEzvx_XkTm5S7nIx02U1aHSaB3kaTM9yhc9JNEmxSxxuYIaMwrSoB_cfE8ck6VTKm5s4HBX2aYcg`
    return config
  })
}

export default httpClient
