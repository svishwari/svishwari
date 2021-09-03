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

  deliveries: {},

  demographics: {},

  geoCities: [],

  geoCountries: [],

  geoStates: [],
}

const getters = {
  list: (state) => Object.values(state.audiences),

  audience: (state) => (id) => {
    return state.audiences[id]
  },

  audiencesRules: (state) => state.constants,

  deliveries: (state) => (id) => {
    const deliveries = state.deliveries[id]
    return deliveries ? Object.values(state.deliveries[id]) : []
  },

  demographics: (state) => state.demographics,

  geoCities: (state) => state.geoCities,

  geoCountries: (state) => state.geoCountries,

  geoStates: (state) => state.geoStates,
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

  SET_DELIVERIES(state, { id, deliveries }) {
    Vue.set(state.deliveries, id, deliveries)
  },

  SET_DEMOGRAPHICS(state, data) {
    state.demographics = data
  },

  SET_GEO_COUNTRIES(state, data) {
    state.geoCountries = data
  },

  SET_GEO_CITIES(state, data) {
    state.geoCities = data
  },

  ADD_GEO_CITIES(state, data) {
    state.geoCities.push(...data)
  },

  SET_GEO_STATES(state, data) {
    state.geoStates = data
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
      let min_age = audienceInsights.min_age
      let max_age = audienceInsights.max_age
      let age = "-"
      if (min_age && max_age && min_age === max_age) {
        age = min_age
      } else if (min_age && max_age) {
        age = `${min_age}-${max_age}`
      } else {
        age = "-"
      }
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
          subtitle: age,
          icon: "mdi-cake-variant",
        },
        {
          title: "Women",
          subtitle:
            audienceInsights.gender_women &&
            audienceInsights.gender_women.toLocaleString("en-US", {
              style: "percent",
              maximumFractionDigits: 2,
            }),
          icon: "mdi-gender-female",
        },
        {
          title: "Men",
          subtitle:
            audienceInsights.gender_men &&
            audienceInsights.gender_men.toLocaleString("en-US", {
              style: "percent",
              maximumFractionDigits: 2,
            }),
          icon: "mdi-gender-male",
        },
        {
          title: "Other",
          subtitle:
            audienceInsights.gender_other &&
            audienceInsights.gender_other.toLocaleString("en-US", {
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

  async addLookalike({ commit }, payload) {
    try {
      const response = await api.lookalike.create(payload)
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

  async getDeliveries({ commit }, id) {
    try {
      const response = await api.audiences.deliveries(id)
      commit("SET_DELIVERIES", {
        audienceId: id,
        deliveries: response.data,
      })
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getDemographics({ commit }, data) {
    try {
      const response = await api.audiences.demographics(data)
      commit("SET_DEMOGRAPHICS", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getGeoCities({ commit }, { id, batchNumber, batchSize }) {
    try {
      if (batchNumber === 1) commit("SET_GEO_CITIES", [])
      const response = await api.audiences.geoCities(id, batchNumber, batchSize)
      commit("ADD_GEO_CITIES", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getGeoCountries({ commit }, id) {
    try {
      const response = await api.audiences.geoCountries(id)
      commit("SET_GEO_COUNTRIES", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getGeoStates({ commit }, id) {
    try {
      const response = await api.audiences.geoStates(id)
      commit("SET_GEO_STATES", response.data)
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
