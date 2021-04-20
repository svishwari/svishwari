import Drawer from "@/components/common/Drawer"
import { mount, shallowMount } from "@vue/test-utils"
import Vuetify from 'vuetify';

const vuetify = new Vuetify();

describe("Drawer", () => {

  test("Drawer calls function on close", async () => {

    const wrapper = mount(Drawer,{
        propsData: {
            value: true,
        },
        vuetify,
    })
    await wrapper.setData({ localDrawer: false })
    expect(  typeof wrapper.emitted().onClose === 'function')
    expect(wrapper).toMatchSnapshot()
  })
})
