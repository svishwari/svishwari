import AlertToast from "./alertToast.vue"

export default {
  component: AlertToast,

  title: "NewComponents/AlertToast",

  argTypes: {
    label: { control: { type: "text" } },
    type: {
      options: [
        "positive",
        "negative",
        "informative",
        "warning",
        "guiding",
        "offline",
      ],
      control: { type: "select" },
    },
  },

  args: {
    label: "This is an alert toast.",
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/nfrkMnYTxnjK5r2NTQqWb9/5.0-Release-06-21?node-id=1826%3A5",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { AlertToast },
  props: Object.keys(argTypes),
  template: `
    <alert-toast v-bind="$props" v-on="$props">
      ${args.default}
    </alert-toast>
  `,
})

export const myAlertToast = Template.bind({})
