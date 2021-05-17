import DescriptiveCard from "@/components/common/cards/DescriptiveCard"
import { shallowMount } from "@vue/test-utils"

describe("Cards", () => {
  describe("Descriptive Card", () => {
    test("Displays custom properties", () => {
      const customProps = {
        icon: "model-unsubscribe",
        title: "Propensity to Unsubscribe",
        description:
          "Propensity of a customer making a purchase after receiving an email.",
      }

      const wrapper = shallowMount(DescriptiveCard, {
        propsData: customProps,
      })

      expect(wrapper.text()).toContain(customProps.title)
      expect(wrapper.text()).toContain(customProps.description)
      expect(wrapper).toMatchSnapshot()
    })

    test("Displays custom slots", () => {
      const customSlots = {
        default: "<p>Default content</p>",
        top: "<div>Top spot</div>",
      }

      const wrapper = shallowMount(DescriptiveCard, {
        slots: customSlots,
      })

      expect(wrapper.find("p").exists()).toBe(true)
      expect(wrapper.find("div").exists()).toBe(true)
      expect(wrapper).toMatchSnapshot()
    })
  })
})
