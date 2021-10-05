//File to be tested
import HuxAlert from "@/components/common/HuxAlert"
//Test utils
import { shallowMount, createLocalVue } from "@vue/test-utils"
//Dependencies
import Store from "@/store/index.js"
import Vuex from "vuex"
import Vuetify from "vuetify"

let vuetify

beforeEach(() => {
  vuetify = new Vuetify()
})

const localVue = createLocalVue()
localVue.use(Vuex)
const store = Store

describe("Hux Alert", () => {
  test("Hux alert displays custom message for error type", async function () {
    let alert = {
      message: "This is a error message!",
      code: 500,
      type: "error",
    }
    // Set alert
    store._actions["alerts/setAlert"][0](alert)
    // Mount component
    const wrapper = shallowMount(HuxAlert, {
      store,
      vuetify,
      localVue,
    })
    // Check length to be 1
    expect(store.getters["alerts/list"].length).toBe(1)
    // Check wrapper contains alert message
    expect(wrapper.text()).toContain(alert.message)

    expect(wrapper).toMatchSnapshot()

    await new Promise((resolve) =>
      setTimeout(() => {
        // Check length to be 0
        expect(store.getters["alerts/list"].length).toBe(0)
        // Check alert is removed after 5 seconds
        expect(wrapper.text()).not.toContain(alert.message)
        resolve()
      }, 5000)
    )
  })
})
