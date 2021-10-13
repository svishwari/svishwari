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
