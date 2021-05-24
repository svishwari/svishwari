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
}

const getters = {
  list: (state) => state.audiences,
  audience: (state) => (id) => {
    return state.audiences[id]
  },
}

const mutations = {
  SET_ALL(state, items) {
    state.audiences = items
  },
  SET_ONE(state, item) {
    Vue.set(state.audiences, item.id, item)
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
          subtitle: audienceInsights.total_customers.toString(),
        },
        {
          title: "Countries",
          subtitle: audienceInsights.total_countries.toString(),
          icon: "mdi-earth",
        },
        {
          title: "US States",
          subtitle: audienceInsights.total_us_states.toString(),
          icon: "mdi-map",
        },
        {
          title: "Cities",
          subtitle: audienceInsights.total_cities.toString(),
          icon: "mdi-map-marker-radius",
        },
        {
          title: "Age",
          subtitle: audienceInsights.min_age + " - " + audienceInsights.max_age,
          icon: "mdi-cake-variant",
        },
        {
          title: "Women",
          subtitle: audienceInsights.gender_women + "%",
          icon: "mdi-gender-female",
        },
        {
          title: "Men",
          subtitle: audienceInsights.gender_men + "%",
          icon: "mdi-gender-male",
        },
        {
          title: "Other",
          subtitle: audienceInsights.gender_other + "%",
          icon: "mdi-gender-male-female",
        },
      ]
      response.data["insightInfo"] = insightInfo
      let history = [
        {
          title: "Last updated",
          subtitle: response.data.update_time,
          shortName: response.data.updated_by,
          fullName: response.data.updated_by,
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
}

export default {
  namespaced,
  state,
  getters,
  mutations,
  actions,
}
