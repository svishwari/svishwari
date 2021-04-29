// import Vue from "vue"
// import { getAllAudiences } from "@/api/resources/audiences"

const state = {
  audiences: [
    {
      audienceName: "Audience Name 1",
      status: "Active",
      size: {
        approxSize: "654K",
        actualSize: "2,345",
      },
      destinations: {
        details: [
          { logo: "../../../assets/images/facebook.png", name: "facebook" },
          { logo: "../../../assets/images/mailchimp.png", name: "MailChimp" },
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
      audienceName: "Audience Name 1",
      status: "Delivering",
      size: {
        approxSize: "654K",
        actualSize: "2,345",
      },
      destinations: {
        details: [
          { logo: "../../../assets/images/facebook.png", name: "facebook" },
          { logo: "../../../assets/images/mailchimp.png", name: "MailChimp" },
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
      audienceName: "Audience Name 1",
      status: "Active",
      size: {
        approxSize: "654K",
        actualSize: "2,345",
      },
      destinations: {
        details: [
          { logo: "../../../assets/images/facebook.png", name: "facebook" },
          { logo: "../../../assets/images/mailchimp.png", name: "MailChimp" },
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
      audienceName: "Audience Name 1",
      status: "Delivering",
      size: {
        approxSize: "654K",
        actualSize: "2,345",
      },
      destinations: {
        details: [
          { logo: "../../../assets/images/facebook.png", name: "facebook" },
          { logo: "../../../assets/images/mailchimp.png", name: "MailChimp" },
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
      audienceName: "Audience Name 1",
      status: "Error",
      size: {
        approxSize: "1000K",
        actualSize: "2,345",
      },
      destinations: {
        details: [
          { logo: "../../../assets/images/facebook.png", name: "facebook" },
          { logo: "../../../assets/images/mailchimp.png", name: "MailChimp" },
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
      audienceName: "Audience Name 1",
      status: "Active",
      size: {
        approxSize: "2K",
        actualSize: "2,345",
      },
      destinations: {
        details: [
          { logo: "../../../assets/images/facebook.png", name: "facebook" },
          { logo: "../../../assets/images/mailchimp.png", name: "MailChimp" },
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
}

const getters = {
  AllAudiences: (state) => {
    return state.audiences
  },
}

const mutations = {
  SET_ALL_AUDIENCES(state, audiences) {
    /*
     *    audiences.forEach((destination) => {
     *       Vue.set(state.audiences, destination._id, destination)
     *    })
     */
    state.audiences = audiences
  },
}

const actions = {
  async getAllAudiences({ commit }) {
    try {
      /*
       *    const response = await getAllAudiences
       *    commit("SET_ALL_AUDIENCES", response.data)
       */
      commit("SET_ALL_AUDIENCES", state.audiences)
    } catch (error) {
      /*
       *    to do item...
       */
    }
  },
}

export default {
  state,
  getters,
  mutations,
  actions,
}
