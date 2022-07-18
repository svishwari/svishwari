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
    isDisabled: { control: "boolean" },
    isHeader: { control: "boolean" },
    isFooter: { control: "boolean" },
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
    isDisabled: false,
    isHeader: true,
    isFooter: true,
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
        ${args.header}
        </template>
        <template #footer>
          ${args.footer}
        </template>
    <text-menu/>
  `,
})

export const textMenuDropdown = Template.bind({})
