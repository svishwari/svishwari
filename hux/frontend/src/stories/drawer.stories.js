import Drawer from "../components/common/Drawer.vue"
import HuxButton from "../components/common/huxButton.vue"
import { action } from "@storybook/addon-actions"
import Icon from "../components/common/Icon.vue"

export default {
  component: Drawer,
  title: "NewComponents/Drawer",
  argTypes: {
    toRight: {
      control: { type: "boolean" },
    },
    width: {
      control: { type: "number" },
    },
    expandedWidth: {
      table: { disable: true },
    },
    expandable: {
      control: { type: "boolean" },
    },
    disableTransition: {
      control: { type: "boolean" },
    },
    contentPadding: {
      control: { type: "text" },
    },
    contentHeaderPadding: {
      control: { type: "text" },
    },
    headerHeight: {
      control: { type: "text" },
    },
    loading: { table: { disable: true } },
    "header-right": { table: { disable: true } },
    "header-left": { table: { disable: true } },
    default: { table: { disable: true } },
    value: { table: { disable: true } },
    "footer-left": { table: { disable: true } },
    "footer-right": { table: { disable: true } },
    input: { table: { disable: true } },
    onClose: { table: { disable: true } },
    iconToggle: { table: { disable: true } },
  },
  args: {
    loading: false,
    width: 400,
  },
  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=11331%3A256832",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { Drawer, HuxButton, Icon },
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
      <template #header-left>
        <div class="pt-2">
          <icon v-if="icon" type="add" size="38"/>
          <h3 style="float: right" class="icon ? mt-1 : mb-2">{{title}}</h3>
        </div>
      </template>

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
drawer.args = {
  title: "Title",
  primaryButtons: 1,
  textField: "x results",
  icon: true,
}
