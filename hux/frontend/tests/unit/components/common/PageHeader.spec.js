import PageHeader from "@/components/PageHeader"
import { shallowMount } from "@vue/test-utils"

describe("Page Header", () => {
  test("Page header displays props content", () => {
    const props = {
      icon: "mdi-plus",
      title: "Welcome back, User",
      bgColor: "red",
    }
    const wrapper = shallowMount(PageHeader, {
      propsData: props,
    })

    expect(wrapper.text()).toContain(props.title)
    expect(wrapper.attributes("style")).toBe(
      `background-color: ${props.bgColor};`
    )
    expect(wrapper).toMatchSnapshot()
  })

  test("Page header displays slots content", () => {
    const descriptionContent = "Description"
    const leftSlotContent = "Left slot"
    const rightSlotContent = "Right slot"

    const wrapper = shallowMount(PageHeader, {
      slots: {
        description: `<div>${descriptionContent}</div>`,
        left: `<div>${leftSlotContent}</div>`,
        right: `<div>${rightSlotContent}</div>`,
      },
    })
    expect(wrapper.text()).toContain(descriptionContent)
    expect(wrapper.text()).toContain(leftSlotContent)
    expect(wrapper.text()).toContain(rightSlotContent)
    expect(wrapper).toMatchSnapshot()
  })

  test("Page header displays both slots and props content", () => {
    const descriptionContent = "Description"
    const leftSlotContent = "Left slot"
    const rightSlotContent = "Right slot"
    const props = {
      icon: "mdi-plus",
      title: "Welcome back, User",
      bgColor: "red",
    }

    const wrapper = shallowMount(PageHeader, {
      slots: {
        description: `<div>${descriptionContent}</div>`,
        left: `<div>${leftSlotContent}</div>`,
        right: `<div>${rightSlotContent}</div>`,
      },
      propsData: props,
    })
    expect(wrapper.text()).toContain(descriptionContent)
    expect(wrapper.text()).toContain(leftSlotContent)
    expect(wrapper.text()).toContain(rightSlotContent)
    expect(wrapper.text()).toContain(props.title)
    expect(wrapper.attributes("style")).toBe(
      `background-color: ${props.bgColor};`
    )
    expect(wrapper).toMatchSnapshot()
  })
})
