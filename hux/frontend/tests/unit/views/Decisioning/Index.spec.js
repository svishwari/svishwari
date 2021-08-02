//File to be tested
import Index from "@/views/Decisioning/Index.vue"
//Test utils
import { mount, createLocalVue } from "@vue/test-utils"
//Store
import Store from "@/store/index.js"
import Vuex from "vuex"
//Miragejs
import { makeServer } from "@/api/mock/server.js"

let server

// models
// const unsubscribeModel = {
//   name: "Propensity to Unsubscribe",
//   status: "Active",
//   type: "unsubscribe",
//   id: "2",
// }

// const ltvModel = {
//   name: "LTV",
//   status: "Pending",
//   type: "ltv",
//   id: "1",
// }

beforeEach(() => {
  server = makeServer()
  // IF WE DONT PROVIDE IT TEST ENVIRONMENT IN THE ABOVE LINE IT WOULD SEED THE SERVER
  // server = makeServer({ environment: "test" })
  // server.create("model", unsubscribeModel)
  // server.create("model", ltvModel)
})

afterEach(() => {
  server.shutdown()
})

const localVue = createLocalVue()
localVue.use(Vuex)
const store = Store

describe("Listing of models", () => {
  test("Models store successfully filled", async function () {
    const wrapper = mount(Index, { store, localVue })
    await waitFor(wrapper, '[class="descriptive-card"]')
    expect(store.state.items.length).toHaveLength(2)
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
