//File to be tested
import Index from "@/views/Decisioning/Index.vue"
//Test utils
import { shallowMount, createLocalVue } from "@vue/test-utils"
//Store
import Store from "@/store/index.js"
import Vuex from "vuex"
import Vuetify from "vuetify"
//Miragejs
import { makeServer } from "@/api/mock/server.js"
import filters from "@/filters"

let server

// models
const unsubscribeModel = {
  name: "Propensity to Unsubscribe",
  status: "Active",
  type: "unsubscribe",
  id: "2",
}

const ltvModel = {
  name: "LTV",
  status: "Pending",
  type: "ltv",
  id: "1",
}
let vuetify

beforeEach(() => {
  // server = makeServer()
  vuetify = new Vuetify()
  // IF WE DONT PROVIDE IT TEST ENVIRONMENT IN THE ABOVE LINE IT WOULD SEED THE SERVER
  server = makeServer({ environment: "test" })
  server.create("model", unsubscribeModel)
  server.create("model", ltvModel)
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
    const wrapper = await shallowMount(Index, { store,vuetify, localVue, sync: false })
    await wrapper.vm.$nextTick()
    console.log(wrapper.html())
    expect(wrapper).toMatchSnapshot();
    console.log(store.getters["models/list"])
    await waitFor(wrapper, '[class="descriptive-card"]')
    // await wrapper.findAll("[class='descriptive-card']")
    // expect(store.getters["models/list"]).toHaveLength(2)
  })
})

// This helper method returns a promise that resolves
// once the selector enters the wrapper's dom.
const waitFor = function (wrapper, selector) {
  return new Promise((resolve) => {
    const timer = setInterval(() => {
      const userEl = wrapper.findAll(selector)
      if (userEl.length > 0) {
        clearInterval(timer)
        resolve()
      }
    }, 100)
  })
}
