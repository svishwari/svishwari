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
  selectedAudience: {},
}

const getters = {
  list: (state) => state.audiences,
  selectedAudience: (state) => {
    return state.selectedAudience
  },
}

const mutations = {
  SET_ALL(state, items) {
    state.audiences = items
  },
  SET_SELECTED_AUDIENCE(state, audience) {
    state.selectedAudience = audience
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
      let insightInfo = [
        {
          title: "Target size",
          subtitle: response.data.audience_insights.total_customerss.toString(),
        },
        {
          title: "Countries",
          subtitle: response.data.audience_insights.total_countries.toString(),
          icon: "mdi-earth",
        },
        {
          title: "US States",
          subtitle: response.data.audience_insights.total_us_states.toString(),
          icon: "mdi-map",
        },
        {
          title: "Cities",
          subtitle: response.data.audience_insights.total_cities.toString(),
          icon: "mdi-map-marker-radius",
        },
        {
          title: "Age",
          subtitle:
            response.data.audience_insights.min_age +
            " - " +
            response.data.audience_insights.max_age,
          icon: "mdi-cake-variant",
        },
        {
          title: "Women",
          subtitle: response.data.audience_insights.gender_women + "%",
          icon: "mdi-gender-female",
        },
        {
          title: "Men",
          subtitle: response.data.audience_insights.gender_men + "%",
          icon: "mdi-gender-male",
        },
        {
          title: "Other",
          subtitle: response.data.audience_insights.gender_other + "%",
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
      commit("SET_SELECTED_AUDIENCE", response.data)
    } catch (error) {
      /*
       *    to do item...
       */
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
