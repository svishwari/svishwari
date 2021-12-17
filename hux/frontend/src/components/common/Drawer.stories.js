import Drawer from "./Drawer.vue"
import HuxButton from "./huxButton.vue"

export default {
  component: Drawer,
  title: "Components",
  argTypes: {
    toRight: {
      control: { type: "boolean" },
    },
    value: {
      control: { type: "boolean" },
    },
    width: {
      control: { type: "number" },
    },
    expandedWidth: {
      control: { type: "number" },
    },
    expandable: {
      control: { type: "boolean" },
    },
    disableTransition: {
      control: { type: "boolean" },
    },
    loading: {
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
  components: { Drawer, HuxButton },
  props: Object.keys(argTypes),
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
    @onClose="toggleDrawer = false"
    @iconToggle=""
  >
    <template #header-left>
      <h3 class="h3">Header</h3>
    </template>

    <template #default>
      <div class="body-1 pa-4">
        Some content
      </div>
    </template>

    <template #footer-left>
      <hux-button
        size="large"
        tile
        variant="white"
        class="btn-border box-shadow-none"
        @click="toggleDrawer=false"
      >
        <span class="primary--text">Cancel &amp; back</span>
      </hux-button>
      <hux-button
        tile
        color="primary"
        @click=""
      >
        Create &amp; add
      </hux-button>
    </template>
  </drawer>
        </div>`,
})

export const drawer = Template.bind({})
