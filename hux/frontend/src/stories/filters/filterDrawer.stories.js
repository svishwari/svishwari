import FilterDrawer from "./FilterDrawer.vue"

export default {
  component: FilterDrawer,
  title: "Design System/Filter",
  argTypes: {}
}

const Template = (args, {argTypes}) => ({
  components: { FilterDrawer },
  props: Object.keys(argTypes),
  template: `
    <filter-drawer></filter-drawer>
  `
})

export const Filter = Template.bind({})