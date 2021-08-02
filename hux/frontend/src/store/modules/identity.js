import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const METRICS = {
  total_records: {
    title: "Total no. of records",
    description: "Total number of input records across all data feeds.",
    format: "numeric",
  },
  match_rate: {
    title: "Match rate",
    description:
      "Percentage of input records that are consolidated into Hux IDs.",
    format: "percentage",
  },
  total_unique_ids: {
    title: "Unique Hux IDs",
    description: "Total Hux IDs that represent an anonymous or known customer.",
    format: "numeric",
  },
  total_unknown_ids: {
    title: "Anonymous IDs",
    description:
      "IDs related to online visitors that have not logged in, typically identified by a browser cookie or device ID.",
    format: "numeric",
  },
  total_known_ids: {
    title: "Known IDs",
    description:
      "IDs related to profiles that contain PII from online or offline engagement: name, postal address, email address, and phone number.",
    format: "numeric",
  },
  total_individual_ids: {
    title: "Individual IDs",
    description:
      "Represents a First Name, Last Name and Address combination, used to identify a customer that lives at an address.",
    format: "numeric",
  },
  total_household_ids: {
    title: "Household IDs",
    description:
      "Represents a Last Name and Address combination, used to identify family members that live at the same address.",
    format: "numeric",
  },
}

const namespaced = true

const state = {
  overview: {},

  dataFeeds: {},
}

const getters = {
  overview: (state) => {
    return Object.keys(METRICS).map((metric) => {
      return {
        title: METRICS[metric].title,
        description: METRICS[metric].description,
        value: state.overview[metric],
        format: METRICS[metric].format,
      }
    })
  },

  dataFeeds: (state) => Object.values(state.dataFeeds),
}

const mutations = {
  SET_OVERVIEW(state, data) {
    state.overview = data
  },

  SET_DATA_FEEDS(state, items) {
    items.forEach((item) => {
      Vue.set(state.dataFeeds, item.datafeed_id, item)
    })
  },
}

const actions = {
  async getOverview({ commit }) {
    try {
      const response = await api.idr.overview()
      commit("SET_OVERVIEW", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getDataFeeds({ commit }) {
    try {
      const response = await api.idr.datafeeds()
      commit("SET_DATA_FEEDS", response.data)
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
