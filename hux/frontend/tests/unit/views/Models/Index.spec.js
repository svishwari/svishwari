//File to be tested
import Index from "@/views/Models/Index.vue"
//Test utils
import { shallowMount, createLocalVue } from "@vue/test-utils"
//Dependencies
import Store from "@/store/index.js"
import Vuex from "vuex"
import Vuetify from "vuetify"
import filters from "@/filters"
//Miragejs
import { makeServer } from "@/api/mock/server.js"
import modelSeeds from "@/api/mock/seeds/model.js"

let server

let vuetify

beforeEach(() => {
  vuetify = new Vuetify()
  server = makeServer({ environment: "test" })
  modelSeeds.forEach((seed) => server.create("model", seed))
})

afterEach(() => {
  server.shutdown()
})

const localVue = createLocalVue()
localVue.use(Vuex)
const store = Store

Object.keys(filters).forEach((filterName) => {
  localVue.filter(filterName, filters[filterName])
})

describe("Listing of models", () => {
  test("Models store successfully filled", async function () {
    const wrapper = shallowMount(Index, {
      store,
      vuetify,
      localVue,
      sync: false,
    })
    // TODO: find a better way to this
    // Here we are manually triggering the api call
    await wrapper.vm.getModels()
    expect(store.getters["models/list"].length).toBe(wrapper.vm.models.length)
    expect(wrapper.find("descriptive-card-stub").exists()).toBe(true)
    expect(wrapper).toMatchSnapshot()
  })
})
