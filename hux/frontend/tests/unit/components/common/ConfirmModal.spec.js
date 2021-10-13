import ConfirmModal from "@/components/common/ConfirmModal"
import Icon from "@/components/common/Icon"
import { shallowMount } from "@vue/test-utils"

describe("Tests Confirm Modal", () => {
  test("Confirm modal calls function on close", async () => {
    const wrapper = shallowMount(ConfirmModal, {
      propsData: {
        value: true,
        icon: "sad-face",
      },
    })
    await wrapper.setData({ localModal: false })
    expect(typeof wrapper.emitted().onClose === "function")
  })

  test("Confirm modal displays props content", () => {
    const props = {
      value: true,
      title: "Title prop",
      rightBtnText: "Button prop",
      body: "Body prop",
      subTitle: "Subtitle prop",
      icon: "sad-face",
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
    const bodyContent = "Body slot"
    const titleSlotContent = "Title slot"
    const footerSlotContent =
      "This is a footer slot that displays at the bottom"
    const subTitleSlotContent =
      "This is a subtitle slot that displays below the title"

    const wrapper = shallowMount(ConfirmModal, {
      propsData: {
        value: true,
        icon: "sad-face",
      },
      slots: {
        body: `<div>${bodyContent}</div>`,
        title: `<div>${titleSlotContent}</div>`,
        footer: `<div>${footerSlotContent}</div>`,
        "sub-title": `<div>${subTitleSlotContent}</div>`,
      },
    })
    expect(wrapper.text()).toContain(bodyContent)
    expect(wrapper.text()).toContain(titleSlotContent)
    expect(wrapper.text()).toContain(footerSlotContent)
    expect(wrapper.text()).toContain(subTitleSlotContent)
    expect(wrapper).toMatchSnapshot()
  })
  test("Confirm modal displays icon content", () => {
    const wrapper = shallowMount(ConfirmModal, {
      propsData: {
        value: true,
        icon: "sad-face",
      },
      stubs: {
        icon: Icon,
      },
    })

    expect(wrapper).toMatchSnapshot()
  })
})
