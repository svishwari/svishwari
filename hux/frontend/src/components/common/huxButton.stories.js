import HuxButton from "./huxButton.vue"

export default {
  component: HuxButton,

  title: "Components/Button",

  argTypes: {
    default: {
      control: {
        type: "text",
      },
    },
    variant: { control: "color" },
  },

  args: {
    variant: "primary",
    isTile: true,
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
