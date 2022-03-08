import FilterDrawer from "./FiltersDrawer.vue"
import FilterPanels from "./FilterPanels.vue"
import FilterPanel from "./FilterPanel.vue"
export default {
  title: "Components/Filters",
  component: FilterDrawer,
  FilterPanels,
  FilterPanel,
}

const Template = ({ ...args }) => ({
  components: { FilterDrawer, FilterPanels, FilterPanel },
  template: `
    <div style="margin-left:1200px">
      <filter-drawer isToggled="true">
        <filter-panels>
          <v-checkbox label="My favorites only"></v-checkbox>
          <v-checkbox label="Audiences I've worked on"></v-checkbox>
          <filter-panel title="Attributes">
            <div class="text-body-1 black--text text--lighten-4 pb-2">MODELS</div>
            <div>
              <v-checkbox label="Age Density"></v-checkbox>
              <v-checkbox label="Propensity to unsubscribe"></v-checkbox>
              <v-checkbox label="Predicted lifetime value"></v-checkbox>
              <v-checkbox label="Propensity to purchase"></v-checkbox>
            </div>
            <br />
            <div class="text-body-1 black--text text--lighten-4 pb-2">
              GENERAL
            </div>
            <div>
              <v-checkbox label="Age"></v-checkbox>
              <v-checkbox label="Email"></v-checkbox>
              <v-checkbox label="Gender"></v-checkbox>
              <v-checkbox label="Country"></v-checkbox>
              <v-checkbox label="State"></v-checkbox>
              <v-checkbox label="City"></v-checkbox>
              <v-checkbox label="Zip"></v-checkbox>
            </div>
          </filter-panel>
        </filter-panels>
      </filters-drawer>
    </div>
  `
})

export const HuxFilter = Template.bind({})