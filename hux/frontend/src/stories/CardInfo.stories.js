import CardInfo from "../components/common/CardInfo.vue"

export default {
  title: "Library/CardInfo",
  component: CardInfo,
  argTypes: {
    title: { control: { type: "text" } },
  },
}

const Template = (args, { argTypes }) => ({
  props: Object.keys(argTypes),
  components: { CardInfo },
  template: `<card-info v-bind="$props">
             </card-info>`,
})

export const Default = Template.bind({})
