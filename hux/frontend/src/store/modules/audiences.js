import Vue from "vue"
// import { getAllAudiences } from "@/api/resources/audiences"

const namespaced = true

const NEW_AUDIENCE = {
  name: "",
  engagements: [],
  attributeRules: [],
  destinations: [],
}

const state = {
  audiences: [
    {
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
      lastDelivered: "Today, 12:00 PM",
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
    },
    {
      audienceId: 2,
      audienceName: "Audience Name 1",
      status: "Delivering",
      size: {
        approxSize: "654K",
        actualSize: "2,345",
      },
      destinations: {
        details: [
          { logo: "facebook", name: "Facebook" },
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
      lastDelivered: "Today, 12:00 PM",
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
    },
    {
      audienceId: 3,
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
          { logo: "salesforce", name: "Salesforce" },
          { logo: "netsuite", name: "netsuite" },
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
      lastDelivered: "Today, 12:00 PM",
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
    },
    {
      audienceId: 4,
      audienceName: "Audience Name 1",
      status: "Delivering",
      size: {
        approxSize: "654K",
        actualSize: "2,345",
      },
      destinations: {
        details: [
          { logo: "facebook", name: "Facebook" },
          { logo: "mailchimp", name: "Mailchimp" },
          { logo: "salesforce", name: "Salesforce" },
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
      lastDelivered: "Today, 12:00 PM",
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
    },
    {
      audienceId: 5,
      audienceName: "Audience Name 1",
      status: "Error",
      size: {
        approxSize: "1000K",
        actualSize: "2,345",
      },
      destinations: {
        details: [
          { logo: "facebook", name: "Facebook" },
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
      lastDelivered: "Today, 12:00 PM",
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
    },
    {
      audienceId: 6,
      audienceName: "Audience Name 1",
      status: "Active",
      size: {
        approxSize: "2K",
        actualSize: "2,345",
      },
      destinations: {
        details: [
          { logo: "facebook", name: "Facebook" },
          { logo: "mailchimp", name: "Mailchimp" },
          { logo: "salesforce", name: "Salesforce" },
          { logo: "netsuite", name: "netsuite" },
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
      lastDelivered: "Today, 12:00 PM",
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
    },
  ],
  newAudience: NEW_AUDIENCE,
}

const getters = {
  AllAudiences: (state) => {
    return Object.values(state.audiences)
  },
  current: (state) => {
    return state.newAudience
  },
}

const mutations = {
  SET_ALL_AUDIENCES(state, audiences) {
    /*
     *    audiences.forEach((destination) => {
     *       Vue.set(state.audiences, destination._id, destination)
     *    })
     */
    audiences.forEach((audience) => {
      Vue.set(state.audiences, audience.audienceId, audience)
    })
  },
}

const actions = {
  async getAllAudiences({ commit }) {
    try {
      /*
       *    const response = await getAllAudiences
       *    commit("SET_ALL_AUDIENCES", response.data)
       */
      const response = {
        data: [...state.audiences],
      }
      commit("SET_ALL_AUDIENCES", response.data)
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
