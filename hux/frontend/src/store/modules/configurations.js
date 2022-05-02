import Vue from "vue"
import api from "@/api/client"
import { handleError } from "@/utils"
import sideMenuOptions from "../sideMenuOptions"

const namespaced = true

const state = {
  configurationModels: [],
  sideBarConfigs: [],
}

const getters = {
  configurationModels: (state) => {
    return state.configurationModels
  },

  sideBarConfigs: (state) => {
    return state.sideBarConfigs
  },
}

const mutations = {
  setConfigurationModels(state, models) {
    Vue.set(state, "configurationModels", models)
  },

  setSideBarConfiguration(state, config) {
    Vue.set(state, "sideBarConfigs", config)
  },
}

const actions = {
  async getConfigModels({ commit }) {
    try {
      const result = await api.configurations.getModules()
      commit("setConfigurationModels", result.data)
    } catch (error) {
      handleError(error)
      throw error
    }
  },

  async getSideBarConfig({ commit }) {
    try {
      const result = await api.configurations.getSideBarConfig()
      result.data.settings = result.data.settings.map((element) => {
        if (!element.children) {
          element = {
            ...element,
            ...sideMenuOptions[element.name.toLowerCase().replaceAll(" ", "")],
          }
        } else {
          element.children = element.children.map((ele) => {
            ele = {
              ...ele,
              ...sideMenuOptions[ele.name.toLowerCase().replaceAll(" ", "")],
            }
            return ele
          })
        }
        return element
      })
      commit("setSideBarConfiguration", result.data.settings)
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
