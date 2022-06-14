import PageHeader from "./PageHeader.vue"

export default {
  component: PageHeader,

  title: "NewComponents/PageHeader",

  argTypes: {
    disabled: { control: { type: "boolean" } },
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/nfrkMnYTxnjK5r2NTQqWb9/5.0-Release-06-21?node-id=1826%3A5",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { PageHeader },
  props: Object.keys(argTypes),
  template: `
    <page-header />
  `,
})

export const DefaultHeader = Template.bind({})
