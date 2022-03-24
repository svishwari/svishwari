import HuxFilterPanel from "./FilterPanel.vue"

export default {
  component: HuxFilterPanel,

  title: "Components/FilterPanel",

  argTypes: {
    default: {
      control: {
        type: "text",
      },
    },
    variant: { control: "color" },
    click: { action: "clicked" },
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
  components: { HuxFilterPanel },
  props: Object.keys(argTypes),
  template: `
    <hux-filter-panel v-bind="$props" v-on="$props">
      ${args.default}
    </hux-filter-panel>
  `,
})

export const FilterPanel = Template.bind({})
