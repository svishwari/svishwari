// import Vue from "vue"
// import { getAllDestinations } from "@/api/resources/destinations"

const state = {
  destinations: [
    {
      logo: "adobe-experience",
      title: "Adobe Experience",
      isAlreadyAdded: false,
      isAvailable: true,
      auth_details: [
        {
          name: "Ad account ID",
          type: "text",
          description: "This field is required for....",
        },
        {
          name: "App ID",
          type: "password",
          description: "This field is required for....",
        },
        {
          name: "Access token",
          type: "password",
          description: "This field is required for....",
        },
        {
          name: "App secret",
          type: "password",
          description: "This field is required for....",
        },
      ],
    },
    {
      logo: "facebook",
      title: "Facebook",
      isAlreadyAdded: true,
      isAvailable: true,
      auth_details: [
        {
          name: "Ad account ID",
          type: "text",
          description: "This field is required for....",
        },
        {
          name: "App ID",
          type: "password",
          description: "This field is required for....",
        },
        {
          name: "Access token",
          type: "password",
          description: "This field is required for....",
        },
        {
          name: "App secret",
          type: "password",
          description: "This field is required for....",
        },
      ],
    },
    {
      logo: "google-ads",
      title: "Google Ads",
      isAlreadyAdded: false,
      isAvailable: true,
      auth_details: [
        {
          name: "App ID",
          type: "password",
          description: "This field is required for....",
        },
        {
          name: "Access token",
          type: "password",
          description: "This field is required for....",
        },
        {
          name: "App secret",
          type: "password",
          description: "This field is required for....",
        },
      ],
    },
    {
      logo: "twilio",
      title: "Twilio",
      isAlreadyAdded: false,
      isAvailable: false,
      auth_details: [
        {
          name: "Ad account ID",
          type: "text",
          description: "This field is required for....",
        },
        {
          name: "App ID",
          type: "password",
          description: "This field is required for....",
        },
        {
          name: "Access token",
          type: "password",
          description: "This field is required for....",
        },
        {
          name: "App secret",
          type: "password",
          description: "This field is required for....",
        },
      ],
    },
    {
      logo: "tableau",
      title: "Tableau",
      isAlreadyAdded: false,
      isAvailable: false,
      auth_details: [
        {
          name: "Ad account ID",
          type: "text",
          description: "This field is required for....",
        },
        {
          name: "App ID",
          type: "password",
          description: "This field is required for....",
        },
        {
          name: "Access token",
          type: "password",
          description: "This field is required for....",
        },
        {
          name: "App secret",
          type: "password",
          description: "This field is required for....",
        },
      ],
    },
  ],
}

const getters = {
  AllDestinations: (state) => {
    return state.destinations
  },
}

const mutations = {
  SET_ALL_DESTINATIONS(state, destinations) {
    /*
     *    destinations.forEach((destination) => {
     *       Vue.set(state.destinations, destination._id, destination)
     *    })
     */
    state.destinations = destinations
  },
}

const actions = {
  async getAllDestinations({ commit }) {
    try {
      /*
       *    const response = await getAllDestinations()
       *    commit("SET_ALL_DESTINATIONS", response.data)
       */
      commit("SET_ALL_DESTINATIONS", state.destinations)
    } catch (error) {
      // this is a TODO item
    }
  },
}

export default {
  state,
  getters,
  mutations,
  actions,
}
