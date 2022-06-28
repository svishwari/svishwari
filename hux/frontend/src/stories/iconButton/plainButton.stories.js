import PlainButton from "./plainButton.vue"

export default {
  component: PlainButton,

  title: "NewComponents/IconButton",

  argTypes: {
    default: {
      control: {
        type: "text",
      },
    },
  },

  args: {
    icon: "setting-gear",
    color: "black",
    iconSize: "27",
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
  components: { PlainButton },
  props: Object.keys(argTypes),
  template: `
    <plain-button v-bind="$props" v-on="$props">
      ${args.default}
    </plain-button>
  `,
})

export const myPlainButton = Template.bind({})
