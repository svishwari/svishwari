import HuxList from "./HuxList.vue"

export default {
  component: HuxList,

  title: "NewComponents/List",

  argTypes: {
    numListItems: { control: { type: "number" } },
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/nfrkMnYTxnjK5r2NTQqWb9/5.0-Release-06-21?node-id=1826%3A5",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { HuxList },
  props: Object.keys(argTypes),
  template: `
    <hux-list v-bind="$props"></hux-list>
  `,
})

export const DefaultList = Template.bind({})
