import Vue from "vue"

const namespaced = true

const state = {
  items: {},
  id: 0,
}

const getters = {
  list: (state) => Object.values(state.items),
}

const mutations = {
  SET_ALERT(state, item) {
    let id = state.id
    item.id = id
    Vue.set(state.items, id, item)
    state.id = id + 1
  },

  REMOVE_ALERT(state, id) {
    Vue.delete(state.items, id)
  },
}

const actions = {
  setAlert({ commit }, alert) {
    let id = state.id
    commit("SET_ALERT", alert)
    setTimeout(() => {
      if (alert.code != 401) {
        commit("REMOVE_ALERT", id)
      }
    }, 5000)
  },
  removeAlert({ commit }, id) {
    commit("REMOVE_ALERT", id)
  },
}

export default {
  namespaced,
  state,
  getters,
  mutations,
  actions,
}
