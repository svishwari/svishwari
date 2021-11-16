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

const PINNING = {
  new_company_ids: "New company IDs",
  filename: "Filename",
  address_id_match: "Address ID match",
  new_household_ids: "New household IDs",
  db_reads: "Database reads",
  company_id_match: "Company ID match",
  db_writes: "Database writes",
  new_address_ids: "New address IDs",
  output_records: "Output records",
  empty_records: "Empty records",
  household_id_match: "Household ID match",
  input_records: "Input records",
  individual_id_match: "Individual ID match",
  pinning_timestamp: "Date & time",
  process_time: "Process time in seconds",
  new_individual_ids: "New individual IDs",
}

const STITCHED = {
  stitched_timestamp: "Time stamp",
  records_source: "Records source",
  merge_rate: "Merge rate",
  match_rate: "Match rate",
  digital_ids_merged: "Digital IDs merged",
  digital_ids_added: "Digital IDs matched",
}

const namespaced = true

const state = {
  overview: {},

  timeFrame: {},

  dataFeeds: {},

  dataFeedReports: {},

  matchingTrends: [],
}

const getters = {
  overview: (state) => {
    return Object.keys(METRICS).map((metric) => {
      return {
        title: METRICS[metric].title,
        description: METRICS[metric].description,
        value:
          "overview" in state.overview
            ? state.overview["overview"][metric]
            : null,
        format: METRICS[metric].format,
      }
    })
  },

  responseTimeFrame: (state) => {
    return state.overview.date_range
  },

  timeFrame: (state) => state.timeFrame,

  dataFeeds: (state) => Object.values(state.dataFeeds),

  dataFeed: (state) => (datafeed_id) => state.dataFeeds[datafeed_id],

  matchingTrends: (state) => state.matchingTrends,

  dataFeedReport: (state) => (datafeed_id) => {
    const report = state.dataFeedReports[datafeed_id]

    if (report) {
      return {
        pinning: Object.keys(PINNING).map((key) => {
          return {
            metric: PINNING[key],
            result: report.pinning[key],
          }
        }),
        stitched: Object.keys(STITCHED).map((key) => {
          return {
            metric: STITCHED[key],
            result: report.stitched[key],
          }
        }),
      }
    }
  },
}

const mutations = {
  SET_OVERVIEW(state, data) {
    state.overview = data
  },

  SET_TIME_FRAME(state, data) {
    state.timeFrame = data
  },

  SET_DATA_FEEDS(state, items) {
    state.dataFeeds = {}

    items.forEach((item) => {
      Vue.set(state.dataFeeds, item.datafeed_id, item)
    })
  },

  SET_DATA_FEED_REPORT(state, { datafeed_id, data }) {
    Vue.set(state.dataFeedReports, datafeed_id, data)
  },

  SET_MATCHING_TRENDS(state, data) {
    state.matchingTrends = data
  },
}

const actions = {
  async getOverview({ commit }, { startDate, endDate }) {
    try {
      const response = await api.idr.overview({
        start_date: startDate,
        end_date: endDate,
      })
      commit("SET_OVERVIEW", response.data)

      if (!startDate && !endDate) {
        commit("SET_TIME_FRAME", response.data["date_range"])
      }
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getDataFeeds({ commit }, { startDate, endDate }) {
    try {
      const response = await api.idr.datafeeds({
        start_date: startDate,
        end_date: endDate,
      })
      commit("SET_DATA_FEEDS", response.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getDataFeedReport({ commit }, datafeed_id) {
    try {
      const response = await api.idr.datafeedReport(datafeed_id)
      commit("SET_DATA_FEED_REPORT", {
        datafeed_id: datafeed_id,
        data: response.data,
      })
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getMatchingTrends({ commit }, { startDate, endDate }) {
    try {
      const response = await api.idr.matchingTrends({
        start_date: startDate,
        end_date: endDate,
      })
      commit("SET_MATCHING_TRENDS", response.data)
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
