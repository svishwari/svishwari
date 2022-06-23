import CardFilter from "./CardFilter.vue"

export default {
  component: CardFilter,
  title: "NewComponents/Filter",
  args: {},
}

const CardFilterTemplate = (args, { argTypes }) => ({
  components: { CardFilter },
  props: Object.keys(argTypes),
  template: `
    <div>
      <card-filter v-bind="$props"/>    
    </div>
  `,
})

export const cardFilter = CardFilterTemplate.bind({})
