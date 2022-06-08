import Drawer from "./Drawer2.vue"
import HuxButton from "@/components/common/huxButton.vue"
import { action } from "@storybook/addon-actions"
import AllIcons from "../icons/Icons"

export default {
  component: Drawer,
  title: "Design System/Drawer",
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
  },
  args: {
    loading: false,
    width: 400,
    title: "Title",
    primaryButtons: 0,
    textField: "x results"
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
        <div class="body-1 pa-4">
          Some content
        </div>
      </template>

      <template #footer-left>
        <div>
          <hux-button
            size="large"
            tile
            variant="white"
            class="btn-border box-shadow-none"
            @click="onCancel()"
          >
            <span class="primary--text">Cancel &amp; back</span>
          </hux-button>
          <span v-if="textField && primaryButtons" class="ml-6">{{textField}}</span>
        </div>
      </template>

      <template #footer-right>
        <div>
          <span v-if="textField && !primaryButtons">{{textField}}</span>
          <hux-button
            v-if="primaryButtons == 2"
            tile
            variant="white"
            class="mr-2 btn-border box-shadow-none"
            @click="onCreate()"
          >
            <span class="primary--text">Create &amp; add</span>
          </hux-button>
          <hux-button
            v-if="primaryButtons > 0"
            tile
            color="primary"
            @click="onCreate()"
          >
            Active
          </hux-button>
        </div>
      </template>
    </drawer>
    </div>`,
})

export const drawer = Template.bind({})

