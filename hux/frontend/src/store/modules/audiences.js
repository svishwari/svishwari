import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

const namespaced = true

const NEW_AUDIENCE = {
  name: "",
  engagements: [],
  attributeRules: [],
  destinations: [],
}

const state = {
  audiences: [],
  newAudience: NEW_AUDIENCE,
  constants: {},
}

const getters = {
  list: (state) => Object.values(state.audiences),
  audience: (state) => (id) => {
    return state.audiences[id]
  },
  audiencesRules: (state) => state.constants,
}

const mutations = {
  SET_ALL(state, items) {
    let getAudience = items.sort(function (a, b) {
      return a.name === b.name ? 0 : a.name < b.name ? -1 : 1
    })
    getAudience.forEach((item) => {
      Vue.set(state.audiences, item.id, item)
    })
  },

  SET_ONE(state, item) {
    Vue.set(state.audiences, item.id, item)
  },
  SET_CONSTANTS(state, item) {
    Vue.set(state, "constants", item)
  },
}

const actions = {
  async getAll({ commit }) {
    try {
      const response = await api.audiences.all()
      commit("SET_ALL", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },
  async getAudienceById({ commit }, id) {
    try {
      const response = await api.audiences.find(id)
      const audienceInsights = response.data.audience_insights
      let insightInfo = [
        {
          title: "Target size",
          subtitle: audienceInsights.total_customers,
        },
        {
          title: "Countries",
          subtitle: audienceInsights.total_countries,
          icon: "mdi-earth",
        },
        {
          title: "US States",
          subtitle: audienceInsights.total_us_states,
          icon: "mdi-map",
        },
        {
          title: "Cities",
          subtitle: audienceInsights.total_cities,
          icon: "mdi-map-marker-radius",
        },
        {
          title: "Age",
          subtitle: audienceInsights.min_age + " - " + audienceInsights.max_age,
          icon: "mdi-cake-variant",
        },
        {
          title: "Women",
          subtitle: audienceInsights.gender_women.toLocaleString("en-US", {
            style: "percent",
            maximumFractionDigits: 2,
          }),
          icon: "mdi-gender-female",
        },
        {
          title: "Men",
          subtitle: audienceInsights.gender_men.toLocaleString("en-US", {
            style: "percent",
            maximumFractionDigits: 2,
          }),
          icon: "mdi-gender-male",
        },
        {
          title: "Other",
          subtitle: audienceInsights.gender_other.toLocaleString("en-US", {
            style: "percent",
            maximumFractionDigits: 2,
          }),
          icon: "mdi-gender-male-female",
        },
      ]
      response.data["insightInfo"] = insightInfo
      let history = [
        {
          title: "Last updated",
          subtitle: response.data.update_time,
          shortName: response.data.updated_by,
          //TODO: this is temporary fix to map created by to updated by
          fullName: response.data.updated_by || response.data.created_by,
        },
        {
          title: "Created",
          subtitle: response.data.create_time,
          shortName: response.data.created_by,
          fullName: response.data.created_by,
        },
      ]
      response.data["audienceHistory"] = history
      commit("SET_ONE", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async add({ commit }, audience) {
    try {
      const response = await api.audiences.create(audience)
      commit("SET_ONE", response.data)
      return response.data
    } catch (error) {
      handleError(error)
      throw error
    }
  },
  async fetchConstants({ commit }) {
    try {
      const response = await api.audiences.getRules()
      commit("SET_CONSTANTS", response.data)
      return response.data
    } catch (error) {
      handleError(error)
      throw error
    }
  },
  async fetchFilterSize(_, filter) {
    try {
      const response = await api.customers.getOverview(filter)
      return response.data
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
