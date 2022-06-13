import Drawer from "./Drawer2.vue"
import HuxButton from "../huxButton/huxButton2.vue"
import { action } from "@storybook/addon-actions"
import AllIcons from "../icons/Icons"

export default {
  component: Drawer,
  title: "NewComponents/Drawer",
  argTypes: {
    width: {
      control: { type: "number" },
    },
    loading: { table: { disable: true } },
    title: { control: { type: "text" } },
    iconType: {
      defaultValue: "mapping",
      options: AllIcons,
      control: {
        type: "select",
      },
    },
    secondaryButtonText: { control: { type: "text" } },
    primaryButtonText: { control: { type: "text" } },
    footerTextField: { control: { type: "text" } },
  },
  args: {
    loading: false,
    width: 400,
    title: "Title",
  },
  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=11331%3A256832",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { Drawer, HuxButton },
  props: Object.keys(argTypes),
  methods: {
    onCancel: action("onCancel"),
    onCreate: action("onCreate"),
    toggleDrawer: action("toggleDrawer"),
    onClose: action("onClose"),
  },
  argTypes: {
    onClose: {},
  },
  data() {
    return {
      toggleDrawer: false,
    }
  },
  template: `
    <div>
    <hux-button @click="toggleDrawer = !toggleDrawer"> Toggle Drawer</hux-button>
    <drawer
      v-model="toggleDrawer"
      v-bind="$props"
      v-on="$props"
      @onClose="onClose()"
    >
      <template #default>
        <div class="body-1 pa-6">
          Some content
        </div>
      </template>
    </drawer>
    </div>`,
})

export const drawer = Template.bind({})
