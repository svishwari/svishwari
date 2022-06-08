import SmallMetricCard from "./SmallMetricCard.vue"
import Icon from "../icons/Icon2.vue"
import EmptyPage from "@/components/common/EmptyPage"
import AllIcons from "@/stories/icons/Icons"

export default {
  component: SmallMetricCard,
  title: "Design System/Cards",
  argTypes: {
    icon: {
      options: AllIcons,
      control: {
        type: "select",
      },
    },
    title: { control: { type: "text" } },
    size: {
      defaultValue: "small",
      options: ["small", "medium", "large"],
      control: {
        type: "select",
      },
    },
    actionMenu: {
      control: { type: "boolean" },
    },
    cardBody: {
      defaultValue: "empty",
      options: ["empty", "error"],
      control: {
        type: "select",
      },
    },
  },
  args: {
    title: "Card Title",
  },
  parameters: {
    design: {
      type: "figma",
      url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=11331%3A256774",
    },
  },
}

const Template = (args, { argTypes }) => ({
  components: { SmallMetricCard, Icon, EmptyPage },
  props: Object.keys(argTypes),
  data() {
    return {}
  },
  template: `
    <div>
      <small-metric-card v-bind="$props">
        <template #body>
          <div v-if="$props.cardBody == 'empty'">Empty content</div>
          <empty-page
            v-else
            type="error-on-screens"
            :size="40"
          >
            <template #title>
              <div>Unavailable</div>
            </template>
            <template #subtitle>
              <div>
                Our team is working hard to fix it. Please be patient and try again soon!
              </div>
            </template>
          </empty-page>
        </template>
      </small-metric-card>
    </div>`,
})

export const smallMetricCard = Template.bind({})
