import Stat from "@/components/common/Cards/Stat"
import { mount } from "@vue/test-utils"

describe("Cards", () => {
  describe("Card Stat", () => {
    test("Displays with custom properties", () => {
      const customProps = {
        label: "Last trained",
        value: "2 hrs ago",
      }

      const wrapper = mount(Stat, {
        propsData: customProps,
        slots: {
          default: "12:45pm",
        },
      })

      expect(wrapper.text()).toContain(customProps.label)
      expect(wrapper.text()).toContain(customProps.value)
      expect(wrapper).toMatchSnapshot()
    })
  })
})
