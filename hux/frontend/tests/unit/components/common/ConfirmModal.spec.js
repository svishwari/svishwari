import ConfirmModal from "@/components/common/ConfirmModal"
import { shallowMount } from "@vue/test-utils"

describe("Tests Confirm Modal", () => {
  test("Confirm modal calls function on close", async () => {
    const wrapper = shallowMount(ConfirmModal, {
      propsData: {
        value: true,
      },
    })
    await wrapper.setData({ localModal: false })
    expect(typeof wrapper.emitted().onClose === "function")
  })

  test("Confirm modal displays props content", () => {
    const props = {
      value: true,
      title: "Title",
      rightBtnText: "Button",
      body: "Body",
      subTitle: "Subtitle",
    }
    const wrapper = shallowMount(ConfirmModal, {
      propsData: props,
    })

    expect(wrapper.text()).toContain(props.title)
    expect(wrapper.text()).toContain(props.rightBtnText)
    expect(wrapper.text()).toContain(props.body)
    expect(wrapper.text()).toContain(props.subTitle)
    expect(wrapper).toMatchSnapshot()
  })

  test("Confirm modal displays slots content", () => {
    const bodyContent = "Body"
    const titleSlotContent = "Title"
    const footerSlotContent = "footer"
    const subTitleSlotContent = "footer"

    const wrapper = shallowMount(ConfirmModal, {
      propsData: {
        value: true,
      },
      slots: {
        body: `<div>${bodyContent}</div>`,
        title: `<div>${titleSlotContent}</div>`,
        footer: `<div>${footerSlotContent}</div>`,
        subTitle: `<div>${subTitleSlotContent}</div>`,
      },
    })
    expect(wrapper.text()).toContain(bodyContent)
    expect(wrapper.text()).toContain(titleSlotContent)
    expect(wrapper.text()).toContain(footerSlotContent)
    expect(wrapper.text()).toContain(subTitleSlotContent)
    expect(wrapper).toMatchSnapshot()
  })
})
