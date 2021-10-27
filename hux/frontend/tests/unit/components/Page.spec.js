import Page from "@/components/Page"
import { shallowMount } from "@vue/test-utils"
import Vuetify from "vuetify"

const vuetify = new Vuetify()

describe("Page", () => {
  test("Should have content in header slot", async () => {
    const headerSlotContent = "Header slot"
    const wrapper = shallowMount(Page, {
      slots: {
        header: `<div>${headerSlotContent}</div>`,
      },
    })
    expect(wrapper.text()).toContain(headerSlotContent)
    expect(wrapper).toMatchSnapshot()
  })
  test("Should have content in footer slot", async () => {
    const footerSlotContent = "Footer slot"
    const wrapper = shallowMount(Page, {
      slots: {
        footer: `<div>${footerSlotContent}</div>`,
      },
    })
    expect(wrapper.text()).toContain(footerSlotContent)
    expect(wrapper).toMatchSnapshot()
  })
})
