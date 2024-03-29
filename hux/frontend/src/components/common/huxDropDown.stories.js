import HuxDropdown from "./HuxDropdown"

export default {
  component: HuxDropdown,

  title: "Components/Select",

  argTypes: {
    label: { control: "text" },
    items: { control: "array" },
    onSelect: { action: "Selected!" },
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
    label: "-- Select a value --",
    items: [
      {
        name: "Item 1",
      },
      { name: "Item 2" },
      {
        name: "Item 3",
      },
    ],
    selected: {},
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=1927%3A11902",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { HuxDropdown },

  props: Object.keys(argTypes),

  methods: {
    onSelectMenuItem(item) {
      this.selected = item
    },
  },

  template: `
    <hux-dropdown
      v-bind="$props" 
      v-on="$props"
      @on-select="onSelectMenuItem"
    />
  `,
})

export const Select = Template.bind({})
