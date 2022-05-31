import HuxButton from "./huxButton2.vue"

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
  },

  args: {
    variant: "primary darken-1",
    isTile: false,
    icon: "mdi-plus",
    iconPosition: "left",
    default: "CTA",
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
