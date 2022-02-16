import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const state = {
  domain: {
    sent: [],
    open_Rate: [],
    delivered_rate: [],
    click_rate: [],
    unsubscribe_rate: [],
    complaints_rate: [],
  },
}

const getters = {
  domainlist: (state) => state.domain,
}

const mutations = {
  SET_DOMAIN(state, data) {
    state.domain.sent = data.sent
    state.domain.open_Rate = data.open_Rate
    state.domain.delivered_rate = data.delivered_rate
    state.domain.click_rate = data.click_rate
    state.domain.unsubscribe_rate = data.unsubscribe_rate
    state.domain.complaints_rate = data.complaints_rate
  },
}

const actions = {
  async getDomain({ commit }) {
    try {
      const response = await api.models.emailDomain()
      commit("SET_DOMAIN", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },
}

export default {
  namespaced,
  state,
  getters,
  mutations,
  actions,
}
