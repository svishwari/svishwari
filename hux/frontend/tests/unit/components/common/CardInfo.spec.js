import CardInfo from "@/components/common/CardInfo"
import { shallowMount } from "@vue/test-utils"

describe("Card Info", () => {
  test("Card info displays a default", () => {
    const defaultProps = {
      icon: "mdi-plus",
      title: "Info card title",
      description: "Info card description",
    }
    const wrapper = shallowMount(CardInfo)

    expect(wrapper.text()).toContain(defaultProps.title)
    expect(wrapper.text()).toContain(defaultProps.description)
    expect(wrapper).toMatchSnapshot()
  })

  test("Card info displays custom properties", () => {
    const customProps = {
      icon: "mdi-facebook",
      title: "Add a Destination",
      description:
        "Choose a destination where your actionable intelligence will be consumed.",
    }

    const wrapper = shallowMount(CardInfo, {
      propsData: customProps,
    })

    expect(wrapper.text()).toContain(customProps.title)
    expect(wrapper.text()).toContain(customProps.description)
    expect(wrapper).toMatchSnapshot()
  })
})
