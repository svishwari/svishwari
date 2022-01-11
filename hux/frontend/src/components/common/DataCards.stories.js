import DataCards from "./DataCards.vue"
import Tooltip from "./Tooltip.vue"
import HuxButton from "./huxButton.vue"

export default {
  component: DataCards,
  title: "Components",
  argTypes: {
    items: {
      control: { type: "array" },
    },

    fields: {
      control: { type: "array" },
    },

    empty: {
      control: { type: "text" },
    },

    sort: {
      control: { type: "text" },
    },

    bordered: {
      control: { type: "boolean" },
    },
    selectedItems: {
      control: { type: "object" },
    },
  },
  args: {
    items: [
      {
        id: 1,
        name: "Item 1",
        size: 40,
      },
      {
        id: 2,
        name: "Item 2",
        size: 30,
      },
      {
        id: 3,
        name: "Item 3",
        size: 20,
      },
    ],
    fields: [
      {
        key: "name",
        label: "Name",
        sortable: true,
        col: "6",
      },
      {
        key: "size",
        label: "Target size",
        sortable: true,
      },
      {
        key: "manage",
        sortable: false,
      },
    ],
    empty: "No audiences have been created.",
    sort: "asc",
    bordered: false,
    selectedItems: () => [],
  },
  parameters: {},
}

const Template = (args, { argTypes }) => ({
  components: { DataCards, Tooltip, HuxButton },
  props: Object.keys(argTypes),
  data() {
    return {}
  },
  template: `
    <div>
      <data-cards
        v-bind="$props"
        v-on="$props"
      >
        <template #field:size="row">
          <tooltip>
            <template #label-content>
              {{ row.value | Numeric(true, true) | Empty }}
            </template>
            <template #hover-content>
              {{
                row.value | Numeric | Empty("Size unavailable at this time")
              }}
            </template>
          </tooltip>
        </template>
        <template #field:manage="row">
          <div class="d-flex align-center justify-end">
            <hux-button
              is-outlined
              variant="primary"
              width="100"
              height="40"
              :box-shadow="false"
            >
              Add
            </hux-button>
          </div>
        </template>
      </data-cards>
    </div>`,
})

export const dataCards = Template.bind({})
