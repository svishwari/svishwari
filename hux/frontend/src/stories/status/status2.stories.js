import Status2 from "./Status2.vue"

export default {
  component: Status2,
  title: "NewComponents/Status2",

  argTypes: {
    status: {
      options: [
        "Active",
        "Delivered",
        "Done",
        "Inactive",
        "Delivery paused",
        "Disabled",
        "Error",
        "Failed",
        "Delivering",
        "Requested",
        "Incomplete",
        "In progress",
        "Not delivered",
        "In review",
        "Canceled",
        "To do",
      ],
      control: "select",
    },
    collapsed: { control: "boolean" },
    showLabel: { control: "boolean" },
    iconSize: { control: "number" },
    tooltipTitle: { control: "text" },
    showIconTooltip: { control: "boolean" },
  },

  args: {
    status: "Active",
    collapsed: "false",
    showLabel: "true",
    iconSize: 16,
    tooltipTitle: "Tooltip title",
    showIconTooltip: "true",
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/eCWUinup52AoHQw1FBVJkd/HDS-(Hux-Design-System)?node-id=9409%3A68520",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { Status2 },
  props: Object.keys(argTypes),
  template: `
  <status2 v-bind="$props"/>`,
})

export const Status = Template.bind({})
