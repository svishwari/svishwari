import TextMenu from "./TextMenu"
import menuItems from "./menuItems.js"

export default {
  component: TextMenu,

  title: "NewComponents/TextMenu",

  argTypes: {
    label: { control: "text" },
    type: { control: "select", options: ["inline", "hotdog", "pill"] },
    header: { control: "text" },
    footer: { control: "text" },
    items: { control: "array" },
    onSelect: { action: "Selected!" },
    isBorder: { control: "boolean" },
    color: {
      table: {
        disable: true,
      },
    },
    isOffsetX: {
      table: {
        disable: true,
      },
    },
    isOffsetY: {
      table: {
        disable: true,
      },
    },
    isOpenOnHover: {
      table: {
        disable: true,
      },
    },
    isSubMenu: {
      table: {
        disable: true,
      },
    },
    transition: {
      table: {
        disable: true,
      },
    },
    icon: {
      table: {
        disable: true,
      },
    },
    "on-select": { table: { disable: true } },
  },

  args: {
    label: "Select item",
    items: menuItems,
    selected: {},
    header: "Header",
    footer: "Text",
    isBorder: true,
    type: "inline",
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=1927%3A11902",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { TextMenu },

  props: Object.keys(argTypes),

  methods: {
    onSelectMenuItem(item) {
      this.selected = item
    },
  },

  template: `
    <text-menu
      v-bind="$props" 
      v-on="$props"
      @on-select="onSelectMenuItem">
        <template #header>
          <div class="text-body-2 pl-4 py-2 font-weight-semi-bold header-class"> ${args.header} </div>
        </template>
        <template #footer>
          <div class="text-body-3 pl-4 py-2 footer-class"> ${args.footer} </div>
        </template>
    <text-menu/>
  `,
})

export const textMenuDropdown = Template.bind({})
