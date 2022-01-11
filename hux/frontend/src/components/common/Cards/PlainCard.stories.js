import PlainCard from "./PlainCard.vue"
import AllIcons from "@/stories/icons/Icons"

export default {
  component: PlainCard,
  title: "Components/Cards",
  argTypes: {
    icon: {
      options: AllIcons,
      control: {
        type: "select",
      },
    },
    title: { control: { type: "text" } },
    description: { control: { type: "text" } },
    disabled: {
      control: { type: "boolean" },
    },
    actionMenu: {
      control: { type: "boolean" },
    },
    comingSoon: { control: { type: "boolean" } },
    height: {
      control: { type: "text" },
    },
    width: {
      control: { type: "text" },
    },
    dotOption: {
      control: { type: "text" },
    },
    logoOption: {
      control: { type: "boolean" },
    },
    iconColor: {
      control: { type: "color" },
    },
  },
  args: {
    icon: "error-on-screen",
    title: "Report a bug",
    description: "Oh no! Did something go wrong? Let’s fix that for you ASAP.",
    disabled: false,
    actionMenu: false,
    comingSoon: false,
    height: "200",
    width: "255",
    dotOption: "Activate",
    logoOption: false,
    iconColor: "white",
  },
  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=11331%3A256774",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { PlainCard },
  props: Object.keys(argTypes),
  data() {
    return {}
  },
  template: `
    <div>
    <plain-card
        v-bind="$props"
        v-on="$props"
        class="my-auto"
      />
        </div>`,
})

export const plainCard = Template.bind({})
