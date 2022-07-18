import SectionalButton from "./SectionalButton.vue"

export default {
  component: SectionalButton,

  title: "NewComponents/SectionalButton",

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/nfrkMnYTxnjK5r2NTQqWb9/5.0-Release-06-21?node-id=1826%3A5",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { SectionalButton },
  props: Object.keys(argTypes),
  template: `
    <sectional-button />
  `,
})

export const ASectionalButton = Template.bind({})
