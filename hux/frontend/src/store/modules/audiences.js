import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"
// import { getAllAudiences } from "@/api/resources/audiences"

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
  selectedAudience: {}
}

const getters = {
  list: (state) => state.audiences,
  selectedAudience: (state) => (id) => {
    return state.selectedAudience[id]
  },
  
}

const mutations = {
  SET_ALL(state, items) {
    state.audiences = items
  },
  SET_SELECTED_AUDIENCE(state, audience) {
    Vue.set(state.selectedAudience, audience.audienceId, audience)
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
      const response = {
        data:  {
            audienceId: 1,
            audienceName: "Audience Name 1",
            status: "Active",
            size: {
              approxSize: "654K",
              actualSize: "2,345",
            },
            destinations: {
              details: [
                { logo: "facebook", name: "Facebook" },
                { logo: "mailchimp", name: "Mailchimp" },
                { logo: "mailchimp", name: "Mailchimp" },
              ],
            },
            attributes: {
              attribute: "Churn +2",
              attributeList: [
                { attribute: "LTV" },
                { attribute: "Propensity" },
                { attribute: "Demgraphics" },
              ],
            },
            lastDelivered: {
              shortDate: "Today, 12:00 PM",
              FullDate: "03/22/2021 12:45 PM",
            },
            lastUpdated: {
              shortDate: "Today, 12:00 PM",
              FullDate: "03/22/2021 12:45 PM",
            },
            lastUpdatedBy: {
              shortName: "HR",
              fullName: "John Smith",
            },
            created: {
              shortDate: "Today, 12:00 PM",
              FullDate: "03/22/2021 12:45 PM",
            },
            createdBy: {
              shortName: "RG",
              fullName: "John Smith",
            },
            overview: [
              { title: "Target size", subtitle: "34,203,204" },
              { title: "Countries", subtitle: "2", icon: "mdi-earth" },
              { title: "US States", subtitle: "52", icon: "mdi-map" },
              { title: "Cities", subtitle: "19,495", icon: "mdi-map-marker-radius" },
              { title: "Age", subtitle: "-", icon: "mdi-cake-variant" },
              { title: "Women", subtitle: "52%", icon: "mdi-gender-female" },
              { title: "Men", subtitle: "46%", icon: "mdi-gender-male" },
              { title: "Other", subtitle: "2%", icon: "mdi-gender-male-female" },
            ],
      
            insightInfo: [
              {
                title: "Last updated",
                subtitle: "Yesterday by",
                shortName: "JS",
                fullName: "John Smith",
              },
              {
                title: "Created",
                subtitle: "Yesterday by",
                shortName: "JS",
                fullName: "John Smith",
              },
            ],
          },
      }
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
