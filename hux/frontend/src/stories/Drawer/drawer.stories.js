import Drawer from "./Drawer2.vue"
import HuxButton from "../huxButton/huxButton2.vue"
import { action } from "@storybook/addon-actions"
import AllIcons from "../icons/Icons"
import Page2 from "../Page/Page2.vue"

export default {
  component: Drawer,
  title: "NewComponents/Drawer",
  argTypes: {
    width: {
      control: { type: "number" },
    },
    loading: { table: { disable: true } },
    title: { control: { type: "text" } },
    drawerContent: { control: { type: "text" } },
    iconType: {
      defaultValue: "mapping",
      options: AllIcons,
      control: {
        type: "select",
      },
    },
    status: {
      control: { type: "select" },
      options: ["Text", "Empty", "Error"],
    },
    secondaryButtonText: { control: { type: "text" } },
    secondPrimaryButtonText: { control: { type: "text" } },
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
  components: { Drawer, HuxButton, Page2 },
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
      <template #drawerContent>
        <div class="new-b1 pa-6" v-if="$props.status == 'Text'">
          {{$props.drawerContent}}
        </div>
        <div class="new-b1 pa-6" v-if="$props.status == 'Error'" >
          <page2 errorState="true" />
        </div>
        <div class="new-b1 pa-6" v-if="$props.status == 'Empty'" >
          <page2 emptyState="true" />
        </div>
      </template>
    </drawer>
    </div>`,
})

export const drawer = Template.bind({})
