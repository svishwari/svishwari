import Vue from "vue"
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
  overview: {},
}

const getters = {
  domainlist: (state) => state.domain,
  getOverview: (state) => state.overview,
}

const mutations = {
  SET_DOMAIN(state, data) {
    state.domain.sent = data.sent
    state.domain.open_rate = data.open_rate
    state.domain.delivered_rate = data.delivered_rate
    state.domain.click_rate = data.click_rate
    state.domain.unsubscribe_rate = data.unsubscribe_rate
    state.domain.complaints_rate = data.complaints_rate
  },
  SET_EMAIL_DELIVERABILITY_OVERVIEW(state, data) {
    Vue.set(state, "overview", data)
  },
}

const actions = {
  async getDomain({ commit }) {
    try {
      const response = await api.emailDeliverability.emailDomain()
      commit("SET_DOMAIN", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },
  async getEmailDeliverabilityOverview({ commit }) {
    try {
      const response = await api.emailDeliverability.getOverview()
      commit("SET_EMAIL_DELIVERABILITY_OVERVIEW", response.data)
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
