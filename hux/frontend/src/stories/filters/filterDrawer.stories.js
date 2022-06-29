import FilterDrawer from "./FilterDrawer.vue"
import testFilterOptions from "./testFilterOptions"

export default {
  component: FilterDrawer,
  title: "NewComponents/Filter",
  args: {
    filterOptions: testFilterOptions,
  },
}

const FilterDrawerTemplate = (args, { argTypes }) => ({
  components: { FilterDrawer },
  props: Object.keys(argTypes),
  template: `
    <filter-drawer v-bind="$props"></filter-drawer>
  `,
})

export const filterDrawer = FilterDrawerTemplate.bind({})
