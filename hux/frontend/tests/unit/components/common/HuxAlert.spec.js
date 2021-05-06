import HuxAlert from "@/components/common/HuxAlert"
import { shallowMount } from "@vue/test-utils"

jest.useFakeTimers()

describe("Hux Alert", () => {
  test("Hux alert displays custom properties", () => {
    const customProps = {
      title: "YAY!",
      message: "This is a success message!",
      value: true,
    }

    const wrapper = shallowMount(HuxAlert, {
      propsData: customProps,
    })

    expect(wrapper.text()).toContain(customProps.title)
    expect(wrapper.text()).toContain(customProps.message)
    expect(wrapper).toMatchSnapshot()
  })
})
