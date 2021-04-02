import axios from 'axios'
import store from '@/store'
/**
 * Create a new Axios client instance
 */
const getClient = () => {
  const options = {
    // baseURL: configEndpoint.serverEndpoint.HOST
  }
  options.headers = {
    'Access-Control-Allow-Origin': '*',
    'Content-Type': 'application/json'
  }

  const client = axios.create(options)

  // Add a request interceptor
  client.interceptors.request.use(
    config => {
      const authStorage = JSON.parse(localStorage.getItem("okta-token-storage"));
      const authToken = authStorage.accessToken.value;
      const authUserName = authStorage.idToken.claims.name;
      config.headers['Authorization'] = `Bearer ${authToken}`
      if (isOktaEnabled == "true") {
          user_name = authUserName;
      }

      if(url.endsWith(configEndpoint.serverEndpoint.fetchModels)){
        config.data.Username = user_name
      }
      else if(url.endsWith(configEndpoint.serverEndpoint.performSegmentation)){        
        config.data.Username = user_name
      }
      else if(url.endsWith(configEndpoint.serverEndpoint.performRealtimeSegmentation)){
        config.data.Username = user_name
      }
      return config
    },
    error => {
      store.commit('LOADING', false)
      return Promise.reject(error)
    }
  )

  client.interceptors.request.use(req => {
    return req
  })

  // Add a response interceptor
  client.interceptors.response.use(
    response => {
      store.commit('LOADING', false)
      return response
    },
    error => {
      store.commit('LOADING', false)
      return Promise.reject(error)
    }
  )
  return client
}

class ApiClient {
  constructor () {
    this.client = getClient()
  }

  get (url, conf = {}) {
    return this.client.get(url, conf)
      .then(response => Promise.resolve(response))
      .catch(error => Promise.reject(error))
  }

  delete (url, conf = {}) {
    return this.client.delete(url, conf)
      .then(response => Promise.resolve(response))
      .catch(error => Promise.reject(error))
  }

  head (url, conf = {}) {
    return this.client.head(url, conf)
      .then(response => Promise.resolve(response))
      .catch(error => Promise.reject(error))
  }

  options (url, conf = {}) {
    return this.client.options(url, conf)
      .then(response => Promise.resolve(response))
      .catch(error => Promise.reject(error))
  }

  post (url, data = {}, conf = {}) {
    return this.client.post(url, data, conf)
      .then(response => Promise.resolve(response))
      .catch(error => Promise.reject(error))
  }

  put (url, data = {}, conf = {}) {
    return this.client.put(url, data, conf)
      .then(response => Promise.resolve(response))
      .catch(error => Promise.reject(error))
  }

  patch (url, data = {}, conf = {}) {
    return this.client.patch(url, data, conf)
      .then(response => Promise.resolve(response))
      .catch(error => Promise.reject(error))
  }
}

export { ApiClient }

/**
 * Base HTTP Client
 */
export default {
  // Provide request methods with the default base_url
  get (url, conf = {}) {
    return getClient().get(url, conf)
      .then(response => Promise.resolve(response))
      .catch(error => Promise.reject(error))
  },

  delete (url, conf = {}) {
    return getClient().delete(url, conf)
      .then(response => Promise.resolve(response))
      .catch(error => Promise.reject(error))
  },

  head (url, conf = {}) {
    return getClient().head(url, conf)
      .then(response => Promise.resolve(response))
      .catch(error => Promise.reject(error))
  },

  options (url, conf = {}) {
    return getClient().options(url, conf)
      .then(response => Promise.resolve(response))
      .catch(error => Promise.reject(error))
  },

  post (url, data = {}, conf = {}) {
    return getClient().post(url, data, conf)
      .then(response => Promise.resolve(response))
      .catch(error => Promise.reject(error))
  },

  put (url, data = {}, conf = {}) {
    return getClient().put(url, data, conf)
      .then(response => Promise.resolve(response))
      .catch(error => Promise.reject(error))
  },

  patch (url, data = {}, conf = {}) {
    return getClient().patch(url, data, conf)
      .then(response => Promise.resolve(response))
      .catch(error => Promise.reject(error))
  }
}
