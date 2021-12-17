import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"
import rules from "../../api/mock/factories/rules.json"

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

  filteredDeliveries: [],

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

  filteredDeliveries: (state) => state.filteredDeliveries,

  demographics: (state) => state.demographics,

  geoCities: (state) => state.geoCities,

  geoCountries: (state) => state.geoCountries,

  geoStates: (state) => state.geoStates,
}

const mutations = {
  SET_ALL(state, items) {
    state.audiences = []
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

  SET_FILTERED_DELIVERIES(state, deliveries) {
    state.filteredDeliveries = deliveries
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

  REMOVE_AUDIENCE(state, id) {
    Vue.delete(state.audiences, id)
  },

  SET_AUDIENCE_LOOKALIKE(state, data) {
    if (!state.audiences[data.id].lookalike_audiences) {
      state.audiences[data.id].lookalike_audiences = []
    }
    state.audiences[data.id].lookalike_audiences.push(data.lookalike)
  },

  UPDATE_LOOKALIKE(state, data) {
    Vue.set(state.audiences[data.id], "name", data.name)
  },
}

const actions = {
  async getAll(
    { commit },
    {
      lookalikeable = false,
      deliveries = 2,
      favorites = false,
      worked_by = false,
      attribute = [],
    }
  ) {
    try {
      const response = await api.audiences.getAudiences({
        lookalikeable: lookalikeable,
        deliveries: deliveries,
        favorites: favorites,
        worked_by: worked_by,
        attribute: attribute,
      })
      commit("SET_ALL", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async fetchAudienceData(_, { id, type }) {
    try {
      const response = await api.audiences.downloadAudience(id, type)
      return response
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
      let response
      if (audience.deliver) {
        delete audience.deliver
        response = await api.audiences.createAndDeliver(audience)
      } else {
        response = await api.audiences.create(audience)
      }
      commit("SET_ONE", response.data)
      return response.data
    } catch (error) {
      handleError(error)
      throw error
    }
  },
  async update({ commit }, { id, payload }) {
    try {
      const response = await api.audiences.update(id, payload)
      commit("SET_ONE", response.data)
      return response.data
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async updateLookalike({ commit, state }, { id, payload }) {
    try {
      const response = await api.lookalike.update(id, payload)
      commit("UPDATE_LOOKALIKE", {
        id: id,
        name: response.data.name,
      })
      return state.audiences[id]
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async remove({ commit }, audience) {
    try {
      await api.audiences.remove(audience.id)
      commit("REMOVE_AUDIENCE", audience.id)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async addLookalike({ commit }, payload) {
    try {
      const response = await api.lookalike.create(payload)
      commit("SET_ONE", response.data)
      commit("SET_AUDIENCE_LOOKALIKE", {
        id: payload.audience_id,
        lookalike: response.data,
      })
      return response.data
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async fetchConstants({ commit }) {
    try {
      const response = await api.audiences.getRules()
      if (response.data.rule_attributes.general.email.options.length === 0) {
        response.data.rule_attributes.general.email.options =
          rules.rule_attributes.general.email.options
      }
      if (response.data.rule_attributes.general.gender.options.length === 0) {
        response.data.rule_attributes.general.gender.options =
          rules.rule_attributes.general.gender.options
      }
      if (
        response.data.rule_attributes.general.location.zip_code.options
          .length === 0
      ) {
        response.data.rule_attributes.general.location.zip_code.options =
          rules.rule_attributes.general.location.zip_code.options
      }
      if (
        response.data.rule_attributes.general.location.city.options.length === 0
      ) {
        response.data.rule_attributes.general.location.city.options =
          rules.rule_attributes.general.location.city.options
      }
      if (
        response.data.rule_attributes.general.location.country.options
          .length === 0
      ) {
        response.data.rule_attributes.general.location.country.options =
          rules.rule_attributes.general.location.country.options
      }
      if (
        response.data.rule_attributes.general.location.state.options.length ===
        0
      ) {
        response.data.rule_attributes.general.location.state.options =
          rules.rule_attributes.general.location.state.options
      }
      commit("SET_CONSTANTS", response.data)
      return response.data
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async fetchFilterSize({ commit }, { filter, overall }) {
    try {
      const response = await api.customers.getOverview(filter)
      if (overall) {
        commit("customers/SET_OVERVIEW", response.data, { root: true })
      }
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
        id: id,
        deliveries: response.data,
      })
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getFilteredDeliveries({ commit }, data) {
    try {
      const response = await api.audiences.deliveries(data.id, data.query)
      commit("SET_FILTERED_DELIVERIES", response.data || [])
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

  async getDensityChartData(_, { field, model }) {
    try {
      const response = await api.audiences.histogram(field, model)
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
