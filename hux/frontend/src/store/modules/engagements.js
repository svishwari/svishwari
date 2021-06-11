import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"

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
    await sleep(2000)
    const response = {
      data: {
        email_audience_performance: {
          summary: {
            sent: 100000,
            hard_bounces: 107,
            hard_bounces_rate: "0.02",
            delivered: 105,
            delivered_rate: "0.60",
            open: 100000,
            open_rate: "0.72",
            clicks: 100000,
            click_through_rate: "0.54",
            click_to_open_rate: "0.06",
            unique_clicks: 100000,
            unique_opens: 100000,
            unsubscribe: 100000,
            unsubscribe_rate: "0.01",
          },
          audience_performance: [
            {
              name: "Audience 1",
              sent: 100000,
              hard_bounces: 227,
              hard_bounces_rate: "0.03",
              delivered: 776,
              delivered_rate: "0.98",
              open: 100000,
              open_rate: "0.89",
              clicks: 100000,
              click_through_rate: "0.81",
              click_to_open_rate: "0.95",
              unique_clicks: 100000,
              unique_opens: 100000,
              unsubscribe: 100000,
              unsubscribe_rate: "0.96",
              campaigns: [
                {
                  name: "Facebook",
                  is_mapped: true,
                  sent: 100000,
                  hard_bounces: 371,
                  hard_bounces_rate: "0.96",
                  delivered: 836,
                  delivered_rate: "0.42",
                  open: 100000,
                  open_rate: "0.34",
                  clicks: 100000,
                  click_through_rate: "0.75",
                  click_to_open_rate: "0.97",
                  unique_clicks: 100000,
                  unique_opens: 100000,
                  unsubscribe: 100000,
                  unsubscribe_rate: "NaN",
                },
                {
                  name: "Facebook",
                  is_mapped: true,
                  sent: 100000,
                  hard_bounces: 812,
                  hard_bounces_rate: "0.98",
                  delivered: 520,
                  delivered_rate: "0.37",
                  open: 100000,
                  open_rate: "0.97",
                  clicks: 100000,
                  click_through_rate: "0.86",
                  click_to_open_rate: "0.41",
                  unique_clicks: 100000,
                  unique_opens: 100000,
                  unsubscribe: 100000,
                  unsubscribe_rate: "NaN",
                },
                {
                  name: "Salesforce Marketing Cloud",
                  is_mapped: true,
                  sent: 100000,
                  hard_bounces: 931,
                  hard_bounces_rate: "0.95",
                  delivered: 752,
                  delivered_rate: "0.79",
                  open: 100000,
                  open_rate: "0.58",
                  clicks: 100000,
                  click_through_rate: "0.32",
                  click_to_open_rate: "0.25",
                  unique_clicks: 100000,
                  unique_opens: 100000,
                  unsubscribe: 100000,
                  unsubscribe_rate: "NaN",
                },
              ],
            },
            {
              name: "Audience 2",
              sent: 100000,
              hard_bounces: 371,
              hard_bounces_rate: "0.68",
              delivered: 572,
              delivered_rate: "0.07",
              open: 100000,
              open_rate: "0.33",
              clicks: 100000,
              click_through_rate: "0.48",
              click_to_open_rate: "0.35",
              unique_clicks: 100000,
              unique_opens: 100000,
              unsubscribe: 100000,
              unsubscribe_rate: "0.60",
              campaigns: [
                {
                  name: "Google-Ads",
                  is_mapped: true,
                  sent: 100000,
                  hard_bounces: 588,
                  hard_bounces_rate: "0.03",
                  delivered: 156,
                  delivered_rate: "0.07",
                  open: 100000,
                  open_rate: "0.53",
                  clicks: 100000,
                  click_through_rate: "0.76",
                  click_to_open_rate: "0.30",
                  unique_clicks: 100000,
                  unique_opens: 100000,
                  unsubscribe: 100000,
                  unsubscribe_rate: "NaN",
                },
                {
                  name: "Facebook",
                  is_mapped: true,
                  sent: 100000,
                  hard_bounces: 264,
                  hard_bounces_rate: "0.28",
                  delivered: 679,
                  delivered_rate: "0.68",
                  open: 100000,
                  open_rate: "0.07",
                  clicks: 100000,
                  click_through_rate: "0.07",
                  click_to_open_rate: "0.96",
                  unique_clicks: 100000,
                  unique_opens: 100000,
                  unsubscribe: 100000,
                  unsubscribe_rate: "NaN",
                },
                {
                  name: "Facebook",
                  is_mapped: true,
                  sent: 100000,
                  hard_bounces: 557,
                  hard_bounces_rate: "0.02",
                  delivered: 302,
                  delivered_rate: "0.40",
                  open: 100000,
                  open_rate: "0.21",
                  clicks: 100000,
                  click_through_rate: "0.87",
                  click_to_open_rate: "0.66",
                  unique_clicks: 100000,
                  unique_opens: 100000,
                  unsubscribe: 100000,
                  unsubscribe_rate: "NaN",
                },
              ],
            },
            {
              name: "Audience 3",
              sent: 100000,
              hard_bounces: 525,
              hard_bounces_rate: "0.51",
              delivered: 871,
              delivered_rate: "0.14",
              open: 100000,
              open_rate: "0.61",
              clicks: 100000,
              click_through_rate: "1.00",
              click_to_open_rate: "0.41",
              unique_clicks: 100000,
              unique_opens: 100000,
              unsubscribe: 100000,
              unsubscribe_rate: "0.90",
              campaigns: [
                {
                  name: "Google-Ads",
                  is_mapped: true,
                  sent: 100000,
                  hard_bounces: 475,
                  hard_bounces_rate: "0.62",
                  delivered: 587,
                  delivered_rate: "0.53",
                  open: 100000,
                  open_rate: "0.45",
                  clicks: 100000,
                  click_through_rate: "0.83",
                  click_to_open_rate: "0.64",
                  unique_clicks: 100000,
                  unique_opens: 100000,
                  unsubscribe: 100000,
                  unsubscribe_rate: "NaN",
                },
                {
                  name: "Facebook",
                  is_mapped: true,
                  sent: 100000,
                  hard_bounces: 367,
                  hard_bounces_rate: "0.33",
                  delivered: 483,
                  delivered_rate: "0.26",
                  open: 100000,
                  open_rate: "0.29",
                  clicks: 100000,
                  click_through_rate: "0.35",
                  click_to_open_rate: "0.38",
                  unique_clicks: 100000,
                  unique_opens: 100000,
                  unsubscribe: 100000,
                  unsubscribe_rate: "NaN",
                },
              ],
            },
          ],
        },
        displayads_audience_performance: {
          summary: {
            spend: 100000,
            reach: 100000,
            impressions: 100000,
            conversions: 100000,
            clicks: 100000,
            frequency: 524,
            cost_per_thousand_impressions: "82.692",
            click_through_rate: 91,
            cost_per_action: 693,
            cost_per_click: 976,
            engagement_rate: "93.779",
          },
          audience_performance: [
            {
              name: "Audience 1",
              spend: 100000,
              reach: 100000,
              impressions: 100000,
              conversions: 100000,
              clicks: 100000,
              frequency: 892,
              cost_per_thousand_impressions: "63.150",
              click_through_rate: 22,
              cost_per_action: 245,
              cost_per_click: 722,
              engagement_rate: "67.528",
              campaigns: [
                {
                  name: "Salesforce Marketing Cloud",
                  is_mapped: true,
                  spend: 100000,
                  reach: 100000,
                  impressions: 100000,
                  conversions: 100000,
                  clicks: 100000,
                  frequency: 210,
                  cost_per_thousand_impressions: "92.489",
                  click_through_rate: 61,
                  cost_per_action: 406,
                  cost_per_click: 664,
                  engagement_rate: "53.477",
                },
                {
                  name: "Facebook",
                  is_mapped: true,
                  spend: 100000,
                  reach: 100000,
                  impressions: 100000,
                  conversions: 100000,
                  clicks: 100000,
                  frequency: 140,
                  cost_per_thousand_impressions: "64.107",
                  click_through_rate: 61,
                  cost_per_action: 431,
                  cost_per_click: 725,
                  engagement_rate: "60.135",
                },
              ],
            },
            {
              name: "Audience 2",
              spend: 100000,
              reach: 100000,
              impressions: 100000,
              conversions: 100000,
              clicks: 100000,
              frequency: 652,
              cost_per_thousand_impressions: "56.017",
              click_through_rate: 71,
              cost_per_action: 605,
              cost_per_click: 904,
              engagement_rate: "85.035",
              campaigns: [
                {
                  name: "Google-Ads",
                  is_mapped: true,
                  spend: 100000,
                  reach: 100000,
                  impressions: 100000,
                  conversions: 100000,
                  clicks: 100000,
                  frequency: 192,
                  cost_per_thousand_impressions: "57.465",
                  click_through_rate: 82,
                  cost_per_action: 809,
                  cost_per_click: 774,
                  engagement_rate: "66.842",
                },
                {
                  name: "Facebook",
                  is_mapped: true,
                  spend: 100000,
                  reach: 100000,
                  impressions: 100000,
                  conversions: 100000,
                  clicks: 100000,
                  frequency: 565,
                  cost_per_thousand_impressions: "69.620",
                  click_through_rate: 56,
                  cost_per_action: 447,
                  cost_per_click: 822,
                  engagement_rate: "55.395",
                },
                {
                  name: "Google-Ads",
                  is_mapped: true,
                  spend: 100000,
                  reach: 100000,
                  impressions: 100000,
                  conversions: 100000,
                  clicks: 100000,
                  frequency: 797,
                  cost_per_thousand_impressions: "62.766",
                  click_through_rate: 77,
                  cost_per_action: 369,
                  cost_per_click: 646,
                  engagement_rate: "76.163",
                },
              ],
            },
            {
              name: "Audience 3",
              spend: 100000,
              reach: 100000,
              impressions: 100000,
              conversions: 100000,
              clicks: 100000,
              frequency: 641,
              cost_per_thousand_impressions: "74.203",
              click_through_rate: 77,
              cost_per_action: 498,
              cost_per_click: 370,
              engagement_rate: "78.333",
              campaigns: [
                {
                  name: "Google-Ads",
                  is_mapped: true,
                  spend: 100000,
                  reach: 100000,
                  impressions: 100000,
                  conversions: 100000,
                  clicks: 100000,
                  frequency: 653,
                  cost_per_thousand_impressions: "84.022",
                  click_through_rate: 71,
                  cost_per_action: 758,
                  cost_per_click: 901,
                  engagement_rate: "50.944",
                },
                {
                  name: "Google-Ads",
                  is_mapped: true,
                  spend: 100000,
                  reach: 100000,
                  impressions: 100000,
                  conversions: 100000,
                  clicks: 100000,
                  frequency: 283,
                  cost_per_thousand_impressions: "53.092",
                  click_through_rate: 78,
                  cost_per_action: 849,
                  cost_per_click: 490,
                  engagement_rate: "86.318",
                },
              ],
            },
          ],
        },
        id: "5",
      },
    }
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
