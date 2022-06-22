import HuxButton from "./huxButton2.vue"
import allIcons from "../icons/Icons"

export default {
  component: HuxButton,

  title: "NewComponents/Button",

  argTypes: {
    default: {
      control: {
        type: "text",
      },
    },
    variant: { type: "select", options: ["default", "secondary", "danger"] },
    click: { action: "clicked" },
    icon: {options: allIcons, control: {type: "select"}},
  },

  args: {
    variant: "primary darken-1",
    isTile: false,
    default: "button",
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/nfrkMnYTxnjK5r2NTQqWb9/5.0-Release-06-21?node-id=1826%3A5",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { HuxButton },
  props: Object.keys(argTypes),
  template: `
    <hux-button v-bind="$props" v-on="$props">
      ${args.default}
    </hux-button>
  `,
})

export const Button = Template.bind({})
