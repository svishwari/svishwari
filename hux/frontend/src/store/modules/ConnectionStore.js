// import Vue from "vue"
// import { getAllDestinations } from "@/api/resources/destinations"

const state = {
  destinations: [
    { logoUrl: "../assets/images/adobe-icon.png", title: "Adobe Experience" },
    { logoUrl: "../assets/images/adobe-icon.png", title: "Facebook" },
    { logoUrl: "../assets/images/adobe-icon.png", title: "Google" },
    { logoUrl: "../assets/images/adobe-icon.png", title: "Twilio" },
    { logoUrl: "../assets/images/adobe-icon.png", title: "Amazon" },
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
    } catch (error) {}
  },
}

export default {
  state,
  getters,
  mutations,
  actions,
}
