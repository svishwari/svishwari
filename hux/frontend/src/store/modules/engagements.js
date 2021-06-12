import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"
import audiencePerformanceMock from "@/api/mock/factories/audiencePerformance"

const namespaced = true

// TODO Remove the below once API Integration is done
const sleep = (ms) => new Promise((res) => setTimeout(res, ms))

const state = {
  items: {},
  audiencePerformance: {},
}

const getters = {
  list: (state) => Object.values(state.items),
  audiencePerformanceByAds: (state) => state.audiencePerformance.ads,
  audiencePerformanceByEmail: (state) => state.audiencePerformance.email,
}

const mutations = {
  SET_ALL(state, items) {
    items.forEach((item) => {
      Vue.set(state.items, item.id, item)
    })
  },

  SET_ONE(state, item) {
    Vue.set(state.items, item.id, item)
  },
  SET_AUDIENCE_PERFORMANCE(state, { item, type }) {
    /**
     * TODO To be revised with actual API call once API is ready for integration.
     * Below logic needs revision
     */
    let audiencePerformanceObject = {}
    if (type === "ads") {
      audiencePerformanceObject = item["displayads_audience_performance"]
    } else {
      audiencePerformanceObject = item["email_audience_performance"]
    }
    Vue.set(state.audiencePerformance, type, audiencePerformanceObject)
  },
}

const actions = {
  async getAll({ commit }) {
    try {
      const response = await api.engagements.all()
      commit("SET_ALL", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async get({ commit }, id) {
    try {
      const response = await api.engagements.find(id)
      commit("SET_ONE", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getAudiencePerformance({ commit }, payload) {
    /**
     * TODO Comment the below code to enable the API Integration
     *  Mock STUB begin here
     */
    await sleep(2000)
    const data = audiencePerformanceMock
    if (typeof data.displayads_audience_performance.summary === "function") {
      data.displayads_audience_performance.summary = data.displayads_audience_performance.summary()
      data.displayads_audience_performance.audience_performance = data.displayads_audience_performance.audience_performance()
      data.email_audience_performance.summary = data.email_audience_performance.summary()
      data.email_audience_performance.audience_performance = data.email_audience_performance.audience_performance()
    }
    const response = {
      data: data,
    }
    /**
     * *  Mock STUB ends here
     *  TODO Uncomment the below code to enable the API Integration
     */
    // const response = await api.engagements.fetchAudiencePerformance(
    //   payload.id,
    //   payload.type
    // )
    commit("SET_AUDIENCE_PERFORMANCE", {
      item: response.data,
      type: payload.type,
    })
  },

  async add({ commit }, engagement) {
    try {
      const payload = {
        name: engagement.name,
        description: engagement.description,
        delivery_schedule:
          engagement.delivery_schedule === 0
            ? null
            : {
                end_date: "",
                start_date: "",
              },
        audiences: Object.values(engagement.audiences).map((audience) => {
          return {
            id: audience.id,
            // TODO: HUS-512
            destinations: [],
          }
        }),
      }
      const response = await api.engagements.create(payload)
      commit("SET_ONE", response.data)
      return response.data
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async update({ commit }, engagement) {
    try {
      const response = await api.engagements.update(
        engagement.id,
        engagement.name,
        engagement.desciption
      )
      commit("SET_ONE", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async deliver(_, id) {
    try {
      await api.engagements.deliver(id)
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
