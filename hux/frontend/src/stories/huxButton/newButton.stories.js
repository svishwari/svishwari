import NewButton from "./NewButton.vue"
import AllIcons from "../icons/Icons"
import AllColors from "../colors/allColors"

export default {
  component: NewButton,

  title: "NewComponents/NewButton",

  argTypes: {
    icon: {
      control: { type: "select" },
      options: AllIcons,
    },
    disabled: { control: { type: "boolean" } },
    danger: { control: { type: "boolean" } },
    variant: {
      control: { type: "select" },
      options: ["primary", "secondary"],
    },
  },

  args: {},

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/nfrkMnYTxnjK5r2NTQqWb9/5.0-Release-06-21?node-id=1826%3A5",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { NewButton },
  props: Object.keys(argTypes),
  template: `
    <new-button v-bind="$props" >
      text
    </new-button>
  `,
})

export const Default = Template.bind({})
