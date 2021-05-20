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
    {
      audienceId: 2,
      audienceName: "Audience Name 2",
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
    {
      audienceId: 3,
      audienceName: "Audience Name 3",
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
    {
      audienceId: 4,
      audienceName: "Audience Name 4",
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
    {
      audienceId: 5,
      audienceName: "Audience Name 5",
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
    {
      audienceId: 6,
      audienceName: "Audience Name 6",
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
      info: [
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
  ],
  newAudience: NEW_AUDIENCE,
}

const getters = {
  AllAudiences: (state) => {
    return Object.values(state.audiences)
  },
  AudienceById: (state) => (id) => {
    return state.audiences.find((audience) => audience.audienceId === id)
  },
  current: (state) => {
    return state.newAudience
  },
}

const mutations = {
  SET_ALL_AUDIENCES(state, audiences) {
    audiences.forEach((audience) => {
      Vue.set(state.audiences, audience.audienceId, audience)
    })
  },
  SET_AUDIENCE(state, data) {
    Vue.set(state.audiences, data.audienceId, data)
  },
}

const actions = {
  async getAllAudiences({ commit }) {
    try {
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
  async getAudienceById({ commit }, id) {
    try {
      const response = state.audiences.find(id)
      commit("SET_AUDIENCE", response.data)
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
