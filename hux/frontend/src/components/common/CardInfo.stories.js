import HuxCardInfo from "./CardInfo.vue"

export default {
  component: HuxCardInfo,

  title: "Components/Card Info",

  argTypes: {},

  args: {
    title: "Create an audience",
    description:
      "Create audiences by segmenting your customer list based on who you wish to target.",
    icon: "mdi-plus",
  },

  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/nfrkMnYTxnjK5r2NTQqWb9/5.0-Release-06-21?node-id=14019%3A178121",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { HuxCardInfo },
  props: Object.keys(argTypes),
  template: `
    <hux-card-info v-bind="$props" v-on="$props">
      ${args.default}
    </hux-card-info>
  `,
})

export const CardInfo = Template.bind({})
