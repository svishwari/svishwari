import FilterDrawer from "./FilterDrawer.vue"
import testFilterOptions from "./testFilterOptions"
import PlainCard from "../cards/PlainCard.vue"
import Icon from "../icons/Icon2.vue"

export default {
  component: FilterDrawer,
  title: "Design System/Filter",
  args: {
    filterOptions: testFilterOptions,
  }
}

const FilterDrawerTemplate = (args, {argTypes}) => ({
  components: { FilterDrawer },
  props: Object.keys(argTypes),
  template: `
    <filter-drawer v-bind="$props"></filter-drawer>
  `
})

export const filterDrawer = FilterDrawerTemplate.bind({})

const CardFilterTemplate = (args, {argTypes}) => ({
  components: { FilterDrawer, PlainCard, Icon },
  props: Object.keys(argTypes),
  data() {
    return {
      toggleFilter: false,
    }
  },
  template: `
    <div>
      <plain-card title="Filter Card">
        <template #call-to-action>
          <span>
            <icon type="filter" size="22" color="primary" @click="toggleFilter = !toggleFilter"/>
          </span>
        </template>
        <template #body>
          <div>{{ toggleFilter ? "true" : "false" }}</div>
        </template>
      </plain-card>
    </div>
  `
})

export const cardFilter = CardFilterTemplate.bind({})