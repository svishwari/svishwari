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
    tooltipContent: { control: { type: "text" } },
    cardBodyText: { control: { type: "text" } },
    isError: { control: { type: "boolean" } },
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
        <template #body v-if="$props.cardBodyText">
          <div>{{ $props.cardBodyText }}</div>
        </template>
      </small-metric-card>
    </div>`,
})

export const smallMetricCard = Template.bind({})
