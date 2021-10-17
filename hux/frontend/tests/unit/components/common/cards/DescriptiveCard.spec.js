import DescriptiveCard from "@/components/common/Cards/DescriptiveCard"
import { shallowMount } from "@vue/test-utils"

describe("Cards", () => {
  describe("Descriptive Card", () => {
    test("Displays custom properties", () => {
      const customProps = {
        icon: "model-unsubscribe",
        title: "Propensity to Unsubscribe",
        description:
          "Propensity of a customer making a purchase after receiving an email.",
        height: "255",
        width: "280"
      }

      const wrapper = shallowMount(DescriptiveCard, {
        propsData: customProps,
      })
      // TODO: since the content is now moved inside tooltip it is stubbing
      // the tooltip and not mounting the title and description in shallowMount
      // mounting the element needs to load alot of dependencies which needs further investigation.
      expect(wrapper).toMatchSnapshot()
    })

    test("Displays custom slots", () => {
      const customProps = {
        height: "255",
        width: "280"
      }
      const customSlots = {
        default: "<p>Default content</p>",
        top: "<div>Top spot</div>",
      }

      const wrapper = shallowMount(DescriptiveCard, {
        slots: customSlots,
        propsData: customProps,
      })

      expect(wrapper.find("p").exists()).toBe(true)
      expect(wrapper.find("div").exists()).toBe(true)
      expect(wrapper).toMatchSnapshot()
    })
  })
})
